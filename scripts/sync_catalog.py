#!/usr/bin/env python3
"""Import documented OpenHytale ID catalogs. Never turn recipe IDs into recipes."""
import argparse
import json
import os
import re
import shutil
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = 'https://openhytale.org/api/'

def fetch(path):
    raise PermissionError('Third-party collection disabled pending explicit rights and owner approval')
    with urllib.request.urlopen(urllib.request.Request(BASE + path, headers={'User-Agent': 'HytaleCraft/1.0'}), timeout=30) as response:
        raw = response.read(8_000_001)
    if len(raw) > 8_000_000:
        raise ValueError('Response too large')
    return json.loads(raw)

def normalize(items, recipe_ids, meta):
    for values in (items, recipe_ids):
        if not isinstance(values, list) or not values or any(not isinstance(v,str) for v in values) or len(values) != len(set(values)):
            raise ValueError('Empty or duplicate catalog')
        if any(not isinstance(v, str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,200}', v) for v in values):
            raise ValueError('Invalid game identifier')
    if not isinstance(meta.get('generated_at'), str):
        raise ValueError('Missing source timestamp')
    def category(i):
        prefix = i.split('_')[0]
        return {'Weapon':'weapons','Armor':'armor','Tool':'tools','Food':'food','Bench':'benches','Furniture':'decor','Plant':'farming','Rock':'building','Wood':'building','Build':'building'}.get(prefix, 'other')
    return {'schema_version': 1, 'source': BASE, 'source_generated_at': meta['generated_at'],
            'game_version': None, 'verification': 'community-extracted-identifiers-only',
            'items': [{'id': i, 'names': {'en': None, 'ru': None}, 'category': category(i)} for i in sorted(items)],
            'recipe_ids': sorted(recipe_ids), 'recipes': [],
            'limitations': ['No recipe bodies, quantities, official names or game build supplied by this API.']}

def save(data, output):
    output = Path(output)
    if output.exists():
        old = json.loads(output.read_text())
        if len(data['items']) < len(old['items']) * .8:
            raise ValueError('Catalog shrank by more than 20%; review manually')
        if old == data:
            return False
        shutil.copy2(output, output.with_suffix('.previous.json'))
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    os.replace(tmp, output)
    return True

def main():
    raise SystemExit('Disabled: no third-party download or public snapshot write. Use import_catalog.py with authorized local JSON; review only.')

if __name__ == '__main__':
    main()
