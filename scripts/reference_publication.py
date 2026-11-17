"""Exact reviewed bounded factual selection; never accepts a full export."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def approved(root=ROOT):
 root=Path(root);p=root/'data/reference-selection.json';a=json.loads((root/'data/reference-selection-approval.json').read_text());raw=p.read_bytes()
 if p.is_symlink() or hashlib.sha256(raw).hexdigest()!=a['sha256']:raise ValueError('Unreviewed reference payload')
 data=json.loads(raw);items=data['items']
 if len(items)!=7 or sum(i['recipe'] is not None for i in items.values())!=4:raise ValueError('Review scope exceeded')
 for key,i in items.items():
  if key!=i['id'] or i['availability']!='unknown' or i['build']!='0.6.4-b27' or i['source_url'] not in ('https://hytale.source.gs/items/iron-sword/','https://hytale.source.gs/items/iron-helm/','https://hytale.source.gs/items/iron-ingot/','https://hytale.source.gs/items/light-leather/','https://hytale.source.gs/items/iron-ore/','https://hytale.source.gs/items/light-hide/'):raise ValueError('Invalid factual provenance')
  if i['recipe']:
   r=i['recipe']
   if r['output_quantity'] is not None or not r['ingredients'] or any(k not in items or type(q)!=int or q<1 for k,q in r['ingredients'].items()):raise ValueError('Unreviewed recipe')
 return data,a,raw
