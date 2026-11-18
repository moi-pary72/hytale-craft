"""Exact reviewed bounded factual selection; never accepts a full export."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EARLY_UPDATE2 = {
 'Weapon_Shield_Iron': (4,3,3,"Armorer's Workbench"),
 'Weapon_Daggers_Iron': (4,2,3,"Blacksmith's Anvil"),
 'Weapon_Mace_Iron': (10,4,3,"Blacksmith's Anvil"),
 'Weapon_Longsword_Iron': (6,4,3,"Blacksmith's Anvil"),
 'Armor_Iron_Chest': (16,7,6,"Armorer's Workbench"),
 'Armor_Iron_Legs': (13,6,4,"Armorer's Workbench"),
 'Tool_Hatchet_Iron': (5,2,2,"Workbench"),
 'Tool_Shovel_Iron': (6,3,2,"Workbench"),
}
EARLY_BUILD = "Hytale Update 2 (January 2026; current build unverified)"
def approved(root=ROOT):
 root=Path(root);p=root/'data/reference-selection.json';a=json.loads((root/'data/reference-selection-approval.json').read_text());raw=p.read_bytes()
 if p.is_symlink() or hashlib.sha256(raw).hexdigest()!=a['sha256']:raise ValueError('Unreviewed reference payload')
 data=json.loads(raw);items=data['items']
 if len(items)!=100 or sum(i['recipe'] is not None for i in items.values())!=13:raise ValueError('Review scope exceeded')
 if sum(i.get('source_name')=='OpenHytale API' for i in items.values())!=84:raise ValueError('Identity selection scope exceeded')
 if sum(i.get('source_name')=='Hytale Item Laboratory' for i in items.values())!=8:raise ValueError('Early build selection scope exceeded')
 for key,i in items.items():
  if i.get('source_name')=='OpenHytale API':
   allowed={'id','names','theme','subcategory','category','visual_family','source_name','source_url','build','observed_on','availability','art','label_origin','classification_basis','recipe'}
   if set(i)!=allowed or key!=i['id'] or i['recipe'] is not None or i['availability']!='unknown' or i['source_url']!='https://openhytale.org/api/catalogs/items.json' or i['build']!='OpenHytale 2026-07-06 (game build unknown)' or i['label_origin']!='derived-from-id':raise ValueError('Identity facts scope exceeded')
   continue
  if i.get('source_name')=='Hytale Item Laboratory':
   reviewed=EARLY_UPDATE2.get(key)
   if not reviewed or key!=i['id'] or i.get('source_url')!='https://hytale.isaacguru.com/wiki/hytale/item/'+key or i.get('build')!=EARLY_BUILD or i.get('availability')!='unknown':raise ValueError('Unreviewed Update 2 identity')
   expected={'Ingredient_Bar_Iron':reviewed[0],'Ingredient_Leather_Light':reviewed[1],'Ingredient_Fabric_Scrap_Linen':reviewed[2]}
   recipe=i.get('recipe')
   if not isinstance(recipe,dict) or recipe.get('ingredients')!=expected or recipe.get('station')!=reviewed[3] or recipe.get('output_quantity')!=1 or recipe.get('status')!='source-documented-complete':raise ValueError('Unreviewed Update 2 recipe')
   allowed={'ingredients','station','output_quantity','status'}
   if key=='Weapon_Mace_Iron':
    allowed.add('alternative_stations')
    if recipe.get('alternative_stations')!=['Forge']:raise ValueError('Incorrect alternative station')
    methods=i.get('methods')
    if not isinstance(methods,list) or len(methods)!=2 or [m.get('id') for m in methods]!=['anvil','forge'] or [m.get('station') for m in methods]!=["Blacksmith's Anvil",'Forge']:raise ValueError('Unreviewed mace methods')
    if any(m.get('ingredients')!=expected or m.get('output_quantity')!=1 or set(m)!={'id','ingredients','station','output_quantity'} for m in methods):raise ValueError('Unreviewed mace details')
   elif 'methods' in i:raise ValueError('Unexpected alternative methods')
   if set(recipe)!=allowed or any(name not in items for name in expected):raise ValueError('Invalid early-build recipe fields')
   continue
  if key!=i['id'] or i['availability']!='unknown' or i['build']!='0.6.4-b27' or i['source_url'] not in ('https://hytale.source.gs/items/iron-pickaxe/','https://hytale.source.gs/items/iron-sword/','https://hytale.source.gs/items/iron-helm/','https://hytale.source.gs/items/iron-ingot/','https://hytale.source.gs/items/light-leather/','https://hytale.source.gs/items/iron-ore/','https://hytale.source.gs/items/light-hide/'):raise ValueError('Invalid factual provenance')
  if i['recipe']:
   r=i['recipe']
   if r['output_quantity'] is not None or not r['ingredients'] or any(k not in items or type(q)!=int or q<1 for k,q in r['ingredients'].items()):raise ValueError('Unreviewed recipe')
 return data,a,raw
