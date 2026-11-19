"""Original item atlas integrity, shared by private/public/standalone assemblers."""
import hashlib,json
from pathlib import Path
TILES=['sword','axe','pickaxe','helmet','breastplate','wood','stone','metal','fabric','plant','food','alchemy','furniture','building','station','neutral']
def intrinsic_webp_dimensions(raw):
 """Read WebP canvas geometry from the container, without a PIL runtime dependency."""
 if len(raw)<30 or raw[:4]!=b'RIFF' or raw[8:12]!=b'WEBP':
  raise ValueError('Item visual WebP header')
 if int.from_bytes(raw[4:8],'little')+8!=len(raw):
  raise ValueError('Item visual WebP RIFF length mismatch')
 chunk=raw[12:16];length=int.from_bytes(raw[16:20],'little')
 if length<10 or 20+length>len(raw):
  raise ValueError('Item visual WebP first chunk truncated')
 if chunk==b'VP8X':
  w=int.from_bytes(raw[24:27],'little')+1
  h=int.from_bytes(raw[27:30],'little')+1
 elif chunk==b'VP8 ':
  if raw[23:26]!=b'\x9d\x01\x2a':
   raise ValueError('Item visual VP8 frame signature')
  w=int.from_bytes(raw[26:28],'little')&0x3fff
  h=int.from_bytes(raw[28:30],'little')&0x3fff
 elif chunk==b'VP8L':
  if raw[20]!=0x2f:raise ValueError('Item visual VP8L frame signature')
  packed=int.from_bytes(raw[21:25],'little')
  w=(packed&0x3fff)+1
  h=((packed>>14)&0x3fff)+1
 else:
  raise ValueError('Unsupported item visual WebP chunk')
 if not 0<w<=16383 or not 0<h<=16383:raise ValueError('Invalid item visual canvas size')
 return w,h

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
  if intrinsic_webp_dimensions(raw)!=(meta.get('width'),meta.get('height')) or meta.get('width')!=1024 or meta.get('height')!=1024:raise ValueError('Item visual atlas intrinsic aspect/dimensions mismatch')
 if len(value.get('extended_tiles',[]))!=16 or len(set(value['extended_tiles']))!=16:raise ValueError('Extended visual contract')
 if len(value.get('crafting_tiles',[]))!=16 or value.get('material_columns')!=['Copper','Iron','Cobalt','Adamantite'] or value.get('material_rows')!=['Sword','Battleaxe','Pickaxe','Head']:raise ValueError('New artwork atlas contract')
 if value.get('weapon_variant_rows')!=['Longsword','Daggers','Mace','Shield'] or value.get('weapon_variant_columns')!=['Copper','Iron','Cobalt','Adamantite']:raise ValueError('Weapon variant atlas contract')
 if value.get('weapon_variant_additions')!=['Weapon_Longsword_Thorium','Weapon_Daggers_Thorium','Weapon_Mace_Thorium','Weapon_Spear_Copper','Weapon_Spear_Iron','Weapon_Spear_Thorium','Weapon_Spear_Cobalt']:raise ValueError('Weapon art additions contract')
 return value
