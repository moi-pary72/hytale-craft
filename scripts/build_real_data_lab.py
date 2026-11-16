#!/usr/bin/env python3
"""Offline local-only research assembly. No fetching, publishing, or rights approval."""
import argparse,gzip,hashlib,json,shutil,sys
from datetime import datetime,timezone
from pathlib import Path
try:
 import sync_recipes as legacy
 import import_catalog as base
 import import_catalog_v2 as schema
except ModuleNotFoundError:
 from scripts import sync_recipes as legacy,import_catalog as base,import_catalog_v2 as schema
ROOT=Path(__file__).resolve().parents[1]

def normalize(manifest,items,recipes,hashes,normalized_on=None):
 # Preserve existing source contract/count/version/ID checks, including historical623 regression.
 old=legacy.normalize(manifest,items,recipes,hashes)
 source='hysphere-research';revision=manifest['revision'];known={r['id'] for r in items['items']}
 def provenance(record,status='unverified'):return {'status':status,'source_id':source,'source_record':record}
 canonical={'schema_version':2,'snapshot':{'game_version':manifest['game']['version'],'channel':'unknown-source-channel','source_revision':revision,'updated_at':manifest['extractedAt']},'sources':[{'id':source,'url':legacy.ORIGIN+'/data','revision':revision,'license':{'id':'Non-commercial-attribution','url':legacy.LICENSE,'commercial_use':'prohibited','redistribution':'unknown','automated_access':'allowed','game_ip_use':'unknown'}}],'items':[],'groups':[],'stations':[],'recipes':[]}
 meta={'items':{},'excluded':[],'raw_hashes':hashes,'exact_build':None,'normalized_on':normalized_on or datetime.now(timezone.utc).date().isoformat(),'attribution':'Data: HySphere — non-commercial local research; underlying Hytale IP remains with Hypixel Studios.','license_url':legacy.LICENSE,'source_url':legacy.ORIGIN+'/data'}
 for row in items['items']:
  canonical['items'].append({'id':row['id'],**provenance('items/'+row['id']),'names':{'en':row.get('name') or None,'ru':None,'es':None,'pt-BR':None},'category':row.get('category') or 'unknown'})
  meta['items'][row['id']]={k:row.get(k) for k in ('hasRecipe','craftRecipeId','quality','itemLevel','obtainHint','categories','parent')}
 stations={}
 for row in recipes['recipes']:
  issues=[]
  for key in ('inputs','outputs'):
   terms=row.get(key)
   if not isinstance(terms,list) or not terms:issues.append('missing_'+key);continue
   ids=[]
   for term in terms:
    item=term.get('itemId');ids.append(item)
    if not item:issues.append('missing_'+key+'_selector')
    elif item not in known:issues.append('unknown_'+key+'_reference')
    if type(term.get('quantity')) is not int or not 0<term['quantity']<=999999:issues.append('invalid_'+key+'_quantity')
   if len(ids)!=len(set(ids)):issues.append('ambiguous_duplicate_'+key)
  benches=row.get('benches')
  if not isinstance(benches,list) or any(not isinstance(b,dict) or (not b.get('id') or b['id'].upper() in ('TODO','UNKNOWN')) for b in benches or []):issues.append('unknown_station')
  if row.get('kind') not in ('craft','salvage'):issues.append('unknown_kind')
  if issues:
   meta['excluded'].append({'id':row['id'],'kind':row.get('kind'),'outputs':[t['itemId'] for t in row.get('outputs',[]) if t.get('itemId') in known],'issues':sorted(set(issues))});continue
  entries=[]
  for b in benches:
   sid=b['id'];stations[sid]={'id':sid,**provenance('benches/'+sid),'names':{'en':sid}}
   entries.append({'station_id':sid,'type':b.get('type') if b.get('type') in ('Crafting','Processing','StructuralCrafting','DiagramCrafting') else 'unknown','min_level':b.get('tier'),'categories':b.get('categories') or [],'augment_tags':[]})
  outputs=[{'item_id':v['itemId'],'quantity':v['quantity']} for v in row['outputs']]
  canonical['recipes'].append({'id':row['id'],**provenance('recipes/'+row['id']),'kind':row['kind'],'inputs':[{'quantity':v['quantity'],'options':[{'kind':'item','id':v['itemId']}]} for v in row['inputs']],'outputs':outputs,'primary_output':row.get('sourceItemId') if row.get('sourceItemId') in [o['item_id'] for o in outputs] else None,'station_requirements':{'mode':'all' if len(entries)==1 else 'unknown','entries':entries},'requirements':{'knowledge_required':row.get('knowledgeRequired'),'memories_level':None},'time_seconds':row.get('timeSeconds')})
 canonical['stations']=list(stations.values());errors,warnings,caps=schema.validate(canonical)
 if errors:raise ValueError('Canonical validation failed: '+str(errors[:5]))
 producers={o['item_id'] for r in canonical['recipes'] for o in r['outputs']}
 meta['blocked_items']=sorted(({i for r in meta['excluded'] for i in r['outputs']}|{i for i,row in meta['items'].items() if row.get('hasRecipe')})-producers)
 meta['metrics']={'items':len(canonical['items']),'source_rows':len(recipes['recipes']),'supported_recipes':len(canonical['recipes']),'legacy_single_output':len(old['recipes']),'multi_output':sum(len(r['outputs'])>1 for r in canonical['recipes']),'excluded_rows':len(meta['excluded']),'stations':len(stations),'source_kind_counts':{k:sum(r.get('kind')==k for r in recipes['recipes']) for k in ['craft','salvage']}}
 meta['validation_warnings']=warnings
 return {'canonical':canonical,'meta':meta,'policy':{'local_only':True,'public_distribution':False,'commercial_use':False,'exact_build_verified':False,'officially_verified':False}}

def build(input_dir,output,acknowledge=False,root=ROOT,normalized_on=None):
 if not acknowledge:raise ValueError('Explicit --local-research-only acknowledgement required; it is not a distribution licence')
 if normalized_on is not None:datetime.strptime(normalized_on,'%Y-%m-%d')
 try:from item_visuals_integrity import verify as verify_visuals
 except ModuleNotFoundError:from scripts.item_visuals_integrity import verify as verify_visuals
 verify_visuals(root)
 root=Path(root);output=base.private_path(output,root);inp=base.private_path(input_dir,root)
 if output.exists():raise ValueError('Use a new private output directory; existing research builds are preserved')
 raw={}
 for k in ('manifest','items','recipes'):
  file=inp/(k+'.json')
  if file.is_symlink():raise ValueError('No source symlinks')
  with file.open('rb') as stream:raw[k]=stream.read(base.MAX_BYTES+1)
 if any(len(v)>base.MAX_BYTES for v in raw.values()):raise ValueError('Research source exceeds bounded importer input')
 hashes={k:hashlib.sha256(v).hexdigest() for k,v in raw.items()};data=normalize(*(base.strict_json(raw[k]) for k in ('manifest','items','recipes')),hashes,normalized_on)
 output.mkdir(parents=True,mode=0o700);files=['web/item-visuals.js','web/item-visuals.css','assets/item-system/categories.webp','web/planner.js','web/planner-v2.js','web/canonical-adapter.js','web/craftable.js','web/beta/workspace.js','web/beta/style.css','web/beta/deep.css','web/lab/adapter.js','web/lab/app.js','web/lab/style.css']
 for name in files:
  path=root/name;dest=output/name;dest.parent.mkdir(parents=True,exist_ok=True)
  if path.is_symlink():raise ValueError('No source symlinks')
  shutil.copyfile(path,dest)
 for directory in ['assets/ui-v2','assets/art-pair']:
  for sourcefile in (root/directory).glob('*.webp'):
   if sourcefile.is_symlink():raise ValueError('No asset symlinks')
   dest=output/directory/sourcefile.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(sourcefile,dest)
 payload=json.dumps(data,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode();base.atomic(output/'research-data.json',payload);(output/'research-data.json').chmod(0o600)
 base.atomic(output/'research-data.json.gz',gzip.compress(payload,mtime=0));(output/'research-data.json.gz').chmod(0o600)
 config={'mode':'local-only','sha256':hashlib.sha256(payload).hexdigest(),'maxBytes':20_000_000,'public_distribution':False}
 (output/'lab-config.js').write_text('window.CRAFT_LAB='+json.dumps(config)+';\n');shutil.copyfile(root/'web/lab/index.html',output/'index.html')
 report={'policy':data['policy'],'metrics':data['meta']['metrics'],'source_revision':data['canonical']['snapshot']['source_revision'],'dataset_sha256':config['sha256'],'raw_sha256':hashes}
 base.atomic(output/'research-report.json',base.encoded(report));return report

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--output',type=Path,default=Path('.private/real-data-lab/build'));p.add_argument('--local-research-only',action='store_true');p.add_argument('--normalized-on');a=p.parse_args();print(json.dumps(build(a.input,a.output,a.local_research_only,normalized_on=a.normalized_on)))
