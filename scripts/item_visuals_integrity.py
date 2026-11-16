"""Original item atlas integrity, shared by private/public/standalone assemblers."""
import hashlib,json
from pathlib import Path
TILES=['sword','axe','pickaxe','helmet','breastplate','wood','stone','metal','fabric','plant','food','alchemy','furniture','building','station','neutral']
def verify(root):
 folder=Path(root)/'assets/item-system';manifest=folder/'manifest.json'
 if manifest.is_symlink():raise ValueError('Visual manifest symlink')
 value=json.loads(manifest.read_text())
 if value.get('schema')!=1 or value.get('tiles')!=TILES or set(value.get('files',{}))!={'categories.webp'}:raise ValueError('Item visual manifest contract')
 p=folder/'categories.webp'
 if p.is_symlink() or not 0<p.stat().st_size<350000:raise ValueError('Item visual asset size/path')
 raw=p.read_bytes()
 if raw[:4]!=b'RIFF' or raw[8:12]!=b'WEBP' or hashlib.sha256(raw).hexdigest()!=value['files']['categories.webp']['sha256']:raise ValueError('Item visual integrity')
 return value
