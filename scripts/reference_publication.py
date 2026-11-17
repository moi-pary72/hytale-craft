"""Exact reviewed bounded factual selection; never accepts a full export."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def approved(root=ROOT):
 root=Path(root);p=root/'data/reference-selection.json';a=json.loads((root/'data/reference-selection-approval.json').read_text());raw=p.read_bytes()
 if p.is_symlink() or hashlib.sha256(raw).hexdigest()!=a['sha256']:raise ValueError('Unreviewed reference payload')
 data=json.loads(raw);items=data['items']
 if len(items)!=100 or sum(i['recipe'] is not None for i in items.values())!=4:raise ValueError('Review scope exceeded')
 if sum(i.get('source_name')=='OpenHytale API' for i in items.values())!=93:raise ValueError('Identity selection scope exceeded')
 for key,i in items.items():
  if i.get('source_name')=='OpenHytale API':
   allowed={'id','names','theme','subcategory','category','visual_family','source_name','source_url','build','observed_on','availability','art','label_origin','classification_basis','recipe'}
   if set(i)!=allowed or key!=i['id'] or i['recipe'] is not None or i['availability']!='unknown' or i['source_url']!='https://openhytale.org/api/catalogs/items.json' or i['build']!='OpenHytale 2026-07-06 (game build unknown)' or i['label_origin']!='derived-from-id':raise ValueError('Identity facts scope exceeded')
   continue
  if key!=i['id'] or i['availability']!='unknown' or i['build']!='0.6.4-b27' or i['source_url'] not in ('https://hytale.source.gs/items/iron-sword/','https://hytale.source.gs/items/iron-helm/','https://hytale.source.gs/items/iron-ingot/','https://hytale.source.gs/items/light-leather/','https://hytale.source.gs/items/iron-ore/','https://hytale.source.gs/items/light-hide/'):raise ValueError('Invalid factual provenance')
  if i['recipe']:
   r=i['recipe']
   if r['output_quantity'] is not None or not r['ingredients'] or any(k not in items or type(q)!=int or q<1 for k,q in r['ingredients'].items()):raise ValueError('Unreviewed recipe')
 return data,a,raw
