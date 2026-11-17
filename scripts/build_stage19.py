#!/usr/bin/env python3
"""Build PRIVATE_REAL_DATA or a rights-safe PUBLIC_RELEASE candidate. Never deploys/downloads."""
import argparse,hashlib,importlib.util,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def module(name):
 s=importlib.util.spec_from_file_location('stage19_'+name,ROOT/'scripts'/(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def build(mode,output,input_dir=None,evidence=None,visuals=None,art=None,acknowledge=False):
 base=module('import_catalog');out=base.private_path(output,ROOT)
 if out.exists():raise ValueError('Output exists; preserve old candidates')
 if mode=='PUBLIC_RELEASE':
  if any(x is not None for x in (input_dir,evidence,visuals,art)):raise ValueError('No research inputs accepted for public mode')
  pages=module('build_pages');public=pages.build('user-only',site_url='https://hytale-craft.pages.dev');audit=module('audit_pages').audit(public);shutil.copytree(public,out);out.chmod(0o700)
  report={'mode':mode,'public_real_items':7,'public_real_recipes':4,'complete_real_recipes':0,'original_learning_methods':8,'noindex':True,'deployed':False,'rights':'Only bounded reviewed factual references; no full foreign catalogue rights','audit_files':audit['files'],'bytes':audit['total_bytes']}
 elif mode=='PRIVATE_REAL_DATA':
  if not acknowledge or input_dir is None:raise ValueError('Private mode needs authorized inputs and --local-research-only')
  verify=module('verify_real_data_lab');report=verify.verify(input_dir,ROOT/'docs/stage18/RESTORE_MANIFEST.json',out);report.update(mode=mode,deployed=False)
  registry=module('build_visual_registry');registry_file=out.parent/(out.name+'-visual-registry.json');report['registry']=registry.build(input_dir,out/'research-data.json',registry_file,evidence)
  if visuals is not None or art is not None:
   if visuals is None or art is None:raise ValueError('Both private visual bindings and original art required')
   vp=base.private_path(visuals,ROOT);ap=base.private_path(art,ROOT);data=base.strict_json(vp.read_bytes())
   if data.get('mode')!='private-research' or data.get('source_revision')!=report['source_revision'] or data.get('original_art_path')!='research-art/items.webp' or hashlib.sha256(ap.read_bytes()).hexdigest()!=data.get('original_art_sha256'):raise ValueError('Private visual provenance/checksum mismatch')
   if len(data.get('entries',[]))>100 or any(e.get('path')!='research-art/items.webp'for e in data['entries']):raise ValueError('Unsafe visual binding paths')
   bundle=base.strict_json((out/'research-data.json').read_bytes());ids={i['id']for i in bundle['canonical']['items']}
   if any(e.get('item_id')not in ids for e in data['entries']):raise ValueError('Visual references absent item')
   (out/'research-art').mkdir();shutil.copyfile(ap,out/'research-art/items.webp');shutil.copyfile(vp,out/'research-visuals.json')
   cfg={'mode':'local-only','sha256':report['dataset_sha256'],'maxBytes':20_000_000,'public_distribution':False,'visualsSha256':hashlib.sha256(vp.read_bytes()).hexdigest(),'source_revision':report['source_revision']}
   (out/'lab-config.js').write_text('window.CRAFT_LAB='+json.dumps(cfg)+';\n');report['private_item_interpretations']=len(data['entries'])
 else:raise ValueError('Unknown build mode')
 base.atomic(out.parent/(out.name+'-build-report.json'),base.encoded(report));return report
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mode',required=True,choices=['PRIVATE_REAL_DATA','PUBLIC_RELEASE']);p.add_argument('--output',required=True,type=Path);p.add_argument('--input',type=Path);p.add_argument('--evidence',type=Path);p.add_argument('--visuals',type=Path);p.add_argument('--art',type=Path);p.add_argument('--local-research-only',action='store_true');a=p.parse_args();print(json.dumps(build(a.mode,a.output,a.input,a.evidence,a.visuals,a.art,a.local_research_only),indent=2))
