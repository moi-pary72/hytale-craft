#!/usr/bin/env python3
"""Offline visual evidence registry. All per-item outputs remain under .private."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
try:from build_real_data_lab import ROOT,base
except ModuleNotFoundError:from scripts.build_real_data_lab import ROOT,base
MATERIALS=('Iron','Copper','Bronze','Steel','Thorium','Cobalt','Adamantite','Mithril','Wood','Stone','Leather','Linen','Wool','Cotton')
def make_registry(bundle,raw_items,evidence=None):
 data=bundle['canonical'];known={i['id']:i for i in data['items']};raw={i['id']:i for i in raw_items['items']}
 if set(raw)!=set(known)or raw_items['extractedAt']!=data['snapshot']['source_revision']:raise ValueError('Visual registry source mismatch')
 producers={};uses={};links={};self_refs={}
 for r in data['recipes']:
  for o in r['outputs']:
   producers.setdefault(o['item_id'],[]).append(r['id'])
   if any(a.get('kind')=='item'and a.get('id')==o['item_id']for s in r['inputs']for a in s['options']):self_refs.setdefault(o['item_id'],[]).append(r['id'])
  for s in r['inputs']:
   for o in s['options']:
    if o['kind']=='item':uses.setdefault(o['id'],set()).add(r['id']);links.setdefault(o['id'],set()).update(x['item_id']for x in r['outputs'])
 blocked=set(bundle['meta']['blocked_items']);rows=[];evidence=evidence or {}
 for item in data['items']:
  id=item['id'];source=raw[id];name=item['names'].get('en')or id;tokens=re.split(r'[^A-Za-z]+',id+' '+name);hints=[v for v in MATERIALS if v.lower()in[t.lower()for t in tokens]]
  ref=evidence.get(id);purpose={'Weapon':'combat','Armor':'protection','Tool':'resource-tool','Bench':'crafting-station','Food':'food','Plant':'plant','Wood':'wood-material','Rock':'rock-material','Cloth':'fabric-material'}.get(item['category'])
  score=5*len(uses.get(id,set()))+min(4,len(producers.get(id,[])))+({'Weapon':30,'Armor':25,'Tool':40,'Bench':45,'Ingredient':20,'Metal':20,'Food':10}.get(item['category'],0))+(100 if ref else 0)
  rows.append({'id':id,'data_provenance':{k:item.get(k)for k in ('source_id','source_record','status')},'names':item['names'],'category':item['category'],'source_primary_group':source.get('primaryGroup'),'source_categories':source.get('categories')or [],'source_tags':source.get('tags')or {},'material':{'confirmed':None,'name_token_hints':hints,'confidence':'unverified-name-hint'if hints else'unknown'},'type':{'source_tags':(source.get('tags')or{}).get('type',[]),'name_key':source.get('nameKey'),'inferred_from_name':[t for t in tokens if t.lower()in {'sword','axe','pickaxe','shortbow','helm','head','hands','legs','boots','chest','ore','ingot','bar','furnace','workbench'}], 'name_hint_status':'not-confirmed-game-type'},'purpose':{'inferred_category_role':purpose,'status':'category-inference'if purpose else'unknown'},'recipe':{'source_has_recipe':source.get('hasRecipe'),'supported_methods':producers.get(id,[]),'incomplete':id in blocked,'self_referential_methods_requiring_review':self_refs.get(id,[])},'used_in_count':len(uses.get(id,set())),'used_in_methods':sorted(uses.get(id,set())),'related_outputs':sorted(links.get(id,set())),'appearance':ref or {'status':'no-item-specific-visual-evidence','confidence':'unknown','silhouette':None,'material':None,'colors':None,'details':None,'publication':'not-approved'},'priority_score':score,'priority_basis':'dependency-use-count plus source-category engineering weights; not player popularity'})
 ranked=sorted(rows,key=lambda r:(-r['priority_score'],r['id']))[:100]
 return {'schema':1,'private_only':True,'source_policy':bundle['policy'],'raw_source_sha256':bundle['meta'].get('raw_hashes',{}),'source_revision':data['snapshot']['source_revision'],'exact_game_build':None,'counts':{'items':len(rows),'supported_methods':len(data['recipes']),'quarantined':len(bundle['meta']['excluded']),'item_visual_evidence':sum(bool(evidence.get(i))for i in known)},'methodology':'No empirical popularity data. Top100 is an engineering/art backlog prioritizing reused ingredients and equipment/stations. Material tokens are NOT confirmed appearance or stats.','items':rows,'priority100':[r['id']for r in ranked]}
def build(input_dir,bundle_path,output,evidence_path=None):
 inp=base.private_path(input_dir,ROOT);bp=base.private_path(bundle_path,ROOT);out=base.private_path(output,ROOT)
 if out.exists():raise ValueError('Registry output exists; preserve prior versions')
 bundle=base.strict_json(bp.read_bytes());items=base.strict_json((inp/'items.json').read_bytes());ev=base.strict_json(base.private_path(evidence_path,ROOT).read_bytes())if evidence_path else{};registry=make_registry(bundle,items,ev);program="const fs=require('node:fs'),v=require(process.argv[1]);const items=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(items.map(i=>v.resolve(i))))";resolved=json.loads(subprocess.run(['node','-e',program,str(ROOT/'web/item-visuals.js')],input=json.dumps(registry['items']),text=True,capture_output=True,check=True).stdout)
 for row,image in zip(registry['items'],resolved):row['visual_resolution']={'generic':image,'individual_research':ev.get(row['id'],{}).get('original_art'),'exact_game_appearance_verified':False}
 registry['counts']['generic_visual_levels']={level:sum(x['level']==level for x in resolved)for level in ('individual','category','neutral')}
 base.atomic(out,base.encoded(registry));out.chmod(0o600)
 return registry['counts']
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('bundle',type=Path);p.add_argument('output',type=Path);p.add_argument('--evidence',type=Path);a=p.parse_args();print(json.dumps(build(a.input,a.bundle,a.output,a.evidence)))
