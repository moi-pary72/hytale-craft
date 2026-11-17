#!/usr/bin/env python3
"""Private batch preparation using the existing canonical-v2 validator. Never publishes."""
import argparse,hashlib,json
from pathlib import Path
try:
 import import_catalog as base
 import import_catalog_v2 as canonical
except ModuleNotFoundError:
 from scripts import import_catalog as base,import_catalog_v2 as canonical

def prepare(source,output):
 source=base.private_path(Path(source),base.ROOT);output=base.private_path(Path(output),base.ROOT)
 if output.exists():raise ValueError('Preserve existing batch; choose a new output directory')
 raw=source.read_bytes()
 if len(raw)>base.MAX_BYTES:raise ValueError('Oversized input')
 bundle=base.strict_json(raw);data=bundle.get('canonical',bundle);errors,warnings,_=canonical.validate(data)
 if errors:raise ValueError('Canonical validation failed; no output written: '+str(len(errors)))
 digest=hashlib.sha256(raw).hexdigest();review_file=base.ROOT/'data/catalog-batch-reviews.json';reviews=json.loads(review_file.read_text()) if review_file.exists() else {};review=reviews.get(digest,{});independent_review=review.get('game_observed') is True and review.get('source_revision')==data['snapshot']['source_revision'];producers={i['id']:[] for i in data['items']};blocked=[];blocked_outputs=set()
 for recipe in data['recipes']:
  self_input=any(any(o['kind']=='item' and o['id']==out['item_id'] for slot in recipe['inputs'] for o in slot['options']) for out in recipe['outputs'])
  if recipe.get('status')=='blocked' or self_input:blocked.append(recipe['id']);blocked_outputs.update(o['item_id'] for o in recipe['outputs']);continue
  for out in recipe['outputs']:producers[out['item_id']].append(recipe)
 counts=dict.fromkeys('ABCD',0);records=[];quarantined=set(bundle.get('meta',{}).get('blocked_items',[]))|blocked_outputs
 for item in data['items']:
  ms=producers[item['id']];complete=[r for r in ms if independent_review and r.get('status')=='verified' and item.get('status')=='verified' and r['station_requirements']['mode']!='unknown' and r['requirements']['knowledge_required'] is not None]
  state='A' if complete else 'B' if ms else 'D' if item.get('status') in ('blocked','incomplete') or item['id'] in quarantined else 'C';counts[state]+=1
  records.append({'id':item['id'],'names':item['names'],'category':item.get('category'),'group':state,'source_id':item['source_id'],'source_record':item['source_record'],'game_version':data['snapshot']['game_version'],'source_revision':data['snapshot']['source_revision'],'methods':[r['id'] for r in ms],'availability':'unknown'})
 report={'schema':1,'input_sha256':hashlib.sha256(raw).hexdigest(),'items':len(records),'groups':counts,'methods':len(data['recipes']),'blocked_methods':blocked,'validation_warnings':warnings,'source_versions_mixed':False,'publication':'requires-independent-rights-and-record-review','group_meaning':{'A':'complete method with independent game observation recorded in trusted batch review','B':'structurally supported source composition; eligibility/version may be unknown','C':'item without supported recipe','D':'incomplete, blocked or quarantined source object'},'source_licences':[{'id':s['id'],'declared_licence':s['license'],'not_publication_approval':True} for s in data['sources']]}
 output.mkdir(parents=True,mode=0o700);base.atomic(output/'records.json',base.encoded({'records':records,'publication':'blocked'}));base.atomic(output/'report.json',base.encoded(report));return report
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=prepare(a.source,a.output);print(json.dumps({k:r[k] for k in ('items','groups','methods','blocked_methods','publication')}))
