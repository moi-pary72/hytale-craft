#!/usr/bin/env python3
"""Package an already-built Hytale Craft research lab for owner's local use.

No scraping, authorization bypass, network upload, or public distribution.
The zip contains normalized private research data and MUST remain private.
"""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
try:
    import import_catalog as base
except ModuleNotFoundError:
    from scripts import import_catalog as base

ROOT = Path(__file__).resolve().parents[1]
SERVER_FILES = ('scripts/import_catalog.py', 'scripts/serve_real_data_lab.py')
REQUIRED = ('index.html', 'lab-config.js', 'research-data.json', 'research-report.json')
BUNDLE_FOLDER = '.private/real-data-lab/owner-build'

README = '''HYTALE CRAFT — ПОЛНЫЙ ЗАКРЫТЫЙ КАТАЛОГ
======================================
Это локальная исследовательская сборка владельца, НЕ официальная база Hytale.
Источник — HySphere, экспорт от 12.08.2026, только некоммерческое исследование;
точная версия игры неизвестна. Данные/сборку нельзя выкладывать на открытый
GitHub, сайты, Cloudflare или отдавать третьим лицам без необходимых прав.

WINDOWS (требуется Python 3): запустите start_windows.cmd.
Либо в папке с распакованным архивом выполните:
    py -3 scripts\\serve_real_data_lab.py .private\\real-data-lab\\owner-build --port 8765
Затем откройте http://127.0.0.1:8765/ на ЭТОМ ЖЕ устройстве.

LINUX / macOS / ANDROID TERMUX (требуется Python 3):
    sh start_local.sh
Откройте http://127.0.0.1:8765/ на том же устройстве.
На Android нужен Termux из официального источника, установленный Python и
распакованный в локальную папку архив. Никакой удалённый сервер не требуется.

Локальный сервер слушает только 127.0.0.1 и отклоняет чужие Host/Origin.
НЕ открывайте доступ через туннель, Wi-Fi/LAN или публичный хостинг.
Инвентарь и пользовательские проекты сохраняются только в браузере устройства.
Иллюстрации категорий — авторские, а не точные игровые иконки.
Полная проверка на физическом Android в этой сессии НЕ выполнялась.
'''
START_SH = '''#!/bin/sh
set -eu
cd "$(dirname "$0")"
exec python3 scripts/serve_real_data_lab.py .private/real-data-lab/owner-build --port 8765
'''
START_WINDOWS = '''@echo off
cd /d "%~dp0"
start "" "http://127.0.0.1:8765/"
py -3 scripts\\serve_real_data_lab.py .private\\real-data-lab\\owner-build --port 8765
pause
'''

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def package(build_dir, output, batch=None, root=ROOT):
    root=Path(root).resolve()
    build=base.private_path(Path(build_dir), root)
    output=base.private_path(Path(output), root)
    if output.exists():
        raise ValueError('Private package already exists; choose a new output filename')
    if not build.is_dir():
        raise ValueError('Private research build not found')
    if any(p.is_symlink() for p in build.rglob('*')):
        raise ValueError('Symlinks are forbidden')
    for name in REQUIRED:
        if not (build/name).is_file():
            raise ValueError('Missing required private build file: '+name)
    config_text=(build/'lab-config.js').read_text(encoding='utf-8').strip()
    match=re.fullmatch(r'window\.CRAFT_LAB\s*=\s*(\{.*\});',config_text)
    if not match:
        raise ValueError('Unrecognized research config')
    config=json.loads(match.group(1))
    if config.get('mode')!='local-only' or config.get('public_distribution') is not False:
        raise ValueError('Research-only policy must remain enforced')
    body=(build/'research-data.json').read_bytes()
    if hashlib.sha256(body).hexdigest()!=config.get('sha256'):
        raise ValueError('Research catalogue checksum mismatch')
    model=json.loads(body)
    if model.get('policy',{}).get('local_only') is not True or model['policy'].get('public_distribution') is not False:
        raise ValueError('Research data is not marked local-only')
    if any((root/x).is_symlink() or not (root/x).is_file() for x in SERVER_FILES):
        raise ValueError('Existing secure local server files missing')
    entries={}
    for item in build.rglob('*'):
        if item.is_file():
            entries[BUNDLE_FOLDER+'/'+item.relative_to(build).as_posix()]=item.read_bytes()
    for name in SERVER_FILES:
        entries[name]=(root/name).read_bytes()
    if batch:
        batch=base.private_path(Path(batch),root)
        for name in ('report.json','records.json'):
            if (batch/name).is_symlink() or not (batch/name).is_file():
                raise ValueError('Invalid private quality batch: '+name)
            entries['private-quality/'+name]=(batch/name).read_bytes()
    entries['README_RU.txt']=README.encode('utf-8')
    entries['start_local.sh']=START_SH.encode('utf-8')
    entries['start_windows.cmd']=START_WINDOWS.encode('utf-8')
    hashes={name:hashlib.sha256(data).hexdigest() for name,data in sorted(entries.items())}
    manifest={'schema':1,'scope':'owner-local-only','no_public_distribution':True,
              'source_revision':model['canonical']['snapshot']['source_revision'],
              'metrics':model['meta']['metrics'],'catalogue_sha256':hashlib.sha256(body).hexdigest(),
              'files_sha256':hashes}
    entries['PRIVATE_PACKAGE_MANIFEST.json']=(json.dumps(manifest,indent=2,ensure_ascii=False,sort_keys=True)+'\n').encode('utf-8')
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as out:
        for name,content in sorted(entries.items()):
            out.writestr(name,content)
    return {'path':str(output),'bytes':output.stat().st_size,'files':len(entries),
            'archive_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'dataset_sha256':manifest['catalogue_sha256'],'metrics':manifest['metrics']}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--quality-batch',type=Path)
    args=parser.parse_args()
    print(json.dumps(package(args.build,args.output,args.quality_batch),ensure_ascii=False))
