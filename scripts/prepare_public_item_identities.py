#!/usr/bin/env python3
"""Prepare a bounded identity-only selection from documented OpenHytale metadata. No recipes, assets or gameplay claims."""
import argparse,hashlib,json
from pathlib import Path
try:from . import import_catalog as base
except ImportError:import import_catalog as base
PIN='d914b5c3e307bea1982cbf3e475a01888118a31914b6193898e14c9cf4d8b181'
MATERIALS={'Copper':['Copper','Медь','Cobre','Cobre'],'Bronze':['Bronze','Бронза','Bronce','Bronze'],'Iron':['Iron','Железо','Hierro','Ferro'],'Thorium':['Thorium','Торий','Torio','Tório'],'Cobalt':['Cobalt','Кобальт','Cobalto','Cobalto'],'Mithril':['Mithril','Мифрил','Mitril','Mithril'],'Adamantite':['Adamantite','Адамантит','Adamantita','Adamantita']}
TYPES={'Sword':('swords','sword',['Sword','Меч','Espada','Espada']),'Longsword':('longswords','sword',['Longsword','Длинный меч','Espada larga','Espada longa']),'Daggers':('daggers','dagger',['Daggers','Кинжалы','Dagas','Adagas']),'Battleaxe':('battleaxes','axe',['Battleaxe','Боевой топор','Hacha de batalla','Machado de batalha']),'Mace':('maces','neutral',['Mace','Булава','Maza','Maça']),'Shortbow':('bows','bow',['Shortbow','Короткий лук','Arco corto','Arco curto']),'Spear':('spears','neutral',['Spear','Копьё','Lanza','Lança']),'Shield':('shields','shield',['Shield','Щит','Escudo','Escudo']),'Head':('helmets','helmet',['Helm','Шлем','Casco','Elmo']),'Chest':('chestpieces','breastplate',['Chest armour','Нагрудник','Peto','Peitoral']),'Hands':('gloves','gauntlets',['Gauntlets','Перчатки','Guanteletes','Manoplas']),'Legs':('legpieces','leggings',['Leg armour','Поножи','Grebas','Grevas']),'Pickaxe':('pickaxes','pickaxe',['Pickaxe','Кирка','Pico','Picareta']),'Hatchet':('hatchets','axe',['Hatchet','Топор','Hacha','Machado']),'Shovel':('shovels','neutral',['Shovel','Лопата','Pala','Pá'])}
def selection(source):
 raw=source.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('Source snapshot changed; review before use')
 ids=base.strict_json(raw)
 if not isinstance(ids,list) or len(ids)!=3641 or any(not isinstance(i,str) for i in ids) or len(ids)!=len(set(ids)):raise ValueError('Unexpected identity schema')
 known=set(ids);data=json.loads((base.ROOT/'data/reference-selection.json').read_text());data['items']={k:v for k,v in data['items'].items() if v.get('source_name')!='OpenHytale API'};items=data['items'];chosen=[]
 for typ in list(TYPES)[:8]:
  chosen.extend((f'Weapon_{typ}_{m}',typ,m,'fight','weapons') for m in MATERIALS if f'Weapon_{typ}_{m}' in known and f'Weapon_{typ}_{m}' not in items)
 for m in MATERIALS:
  chosen.extend((f'Armor_{m}_{typ}',typ,m,'defend','armor') for typ in ['Head','Chest','Hands','Legs'] if f'Armor_{m}_{typ}' in known and f'Armor_{m}_{typ}' not in items)
 tools=[(f'Tool_{typ}_{m}',typ,m,'gather','tools') for typ in ['Pickaxe','Hatchet','Shovel'] for m in MATERIALS if f'Tool_{typ}_{m}' in known];chosen.extend(tools[:15])
 if len(chosen)!=93:raise ValueError('Selection scope changed')
 for key,typ,mat,theme,category in chosen:
  sub,family,labels=TYPES[typ];materials=MATERIALS[mat];names={lang:(materials[k]+' '+labels[k] if k==0 else labels[k]+' · '+materials[k]) for k,lang in enumerate(['en','ru','es','pt-BR'])}
  items[key]={'id':key,'names':names,'theme':theme,'subcategory':sub,'category':category,'visual_family':family,'source_name':'OpenHytale API','source_url':'https://openhytale.org/api/catalogs/items.json','build':'OpenHytale 2026-07-06 (game build unknown)','observed_on':'2026-11-17','availability':'unknown','art':'original-category-illustration','label_origin':'derived-from-id','classification_basis':'structured-id-type; not gameplay or progression verification','recipe':None}
 data['basis']='Seven existing bounded factual references plus93 curated descriptive identity facts from a documented tool-consumable API. No source prose, images, full export or additional recipes.';data['source_notes']={'openhytale':{'metadata_generated_at':'2026-07-06T11:57:22.295504Z','source_sha256':PIN,'identity_only':True,'usage_statement':'https://openhytale.org/developers/','rights_scope':'bounded descriptive public tool, no monetization; not a commercial dataset or game-asset licence'}}
 return data
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();source=base.private_path(a.source,base.ROOT);out=base.private_path(a.output,base.ROOT)
 if out.exists():raise SystemExit('Preserve previous candidate')
 data=selection(source);out.parent.mkdir(parents=True,exist_ok=True);base.atomic(out,(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode());print(json.dumps({'items':len(data['items']),'identity_only_added':93,'new_recipes':0,'review_before_publication':True}))
