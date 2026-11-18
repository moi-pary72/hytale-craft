"""Original item atlas integrity, shared by private/public/standalone assemblers."""
import hashlib,json
from pathlib import Path
TILES=['sword','axe','pickaxe','helmet','breastplate','wood','stone','metal','fabric','plant','food','alchemy','furniture','building','station','neutral']
def verify(root):
 folder=Path(root)/'assets/item-system';manifest=folder/'manifest.json'
 if manifest.is_symlink():raise ValueError('Visual manifest symlink')
 value=json.loads(manifest.read_text())
 if value.get('schema')!=1 or value.get('tiles')!=TILES or set(value.get('files',{}))!={'categories.webp','extended.webp','crafting.webp','materials.webp','weapon-variants.webp','weapon-variants-additions.webp'}:raise ValueError('Item visual manifest contract')
 for name,meta in value['files'].items():
  p=folder/name
  if p.is_symlink() or not 0<p.stat().st_size<350000:raise ValueError('Item visual asset size/path')
  raw=p.read_bytes()
  if raw[:4]!=b'RIFF' or raw[8:12]!=b'WEBP' or hashlib.sha256(raw).hexdigest()!=meta['sha256']:raise ValueError('Item visual integrity')
 if len(value.get('extended_tiles',[]))!=16 or len(set(value['extended_tiles']))!=16:raise ValueError('Extended visual contract')
 if len(value.get('crafting_tiles',[]))!=16 or value.get('material_columns')!=['Copper','Iron','Cobalt','Adamantite'] or value.get('material_rows')!=['Sword','Battleaxe','Pickaxe','Head']:raise ValueError('New artwork atlas contract')
 if value.get('weapon_variant_rows')!=['Longsword','Daggers','Mace','Shield'] or value.get('weapon_variant_columns')!=['Copper','Iron','Cobalt','Adamantite']:raise ValueError('Weapon variant atlas contract')
 if value.get('weapon_variant_additions')!=['Weapon_Longsword_Thorium','Weapon_Daggers_Thorium','Weapon_Mace_Thorium','Weapon_Spear_Copper','Weapon_Spear_Iron','Weapon_Spear_Thorium','Weapon_Spear_Cobalt']:raise ValueError('Weapon art additions contract')
 return value
