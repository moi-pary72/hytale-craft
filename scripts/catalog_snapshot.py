#!/usr/bin/env python3
"""Private immutable canonical-v2 snapshots. Never grants publication permission."""
import argparse,hashlib,json
from pathlib import Path
try:
    import import_catalog as base
    import import_catalog_v2 as importer
except ModuleNotFoundError:
    from scripts import import_catalog as base,import_catalog_v2 as importer

def stage(source,root=base.ROOT,allow_version_change=False):
    root=Path(root);folder=root/'.private/catalog-snapshots';index=base.private_path(folder/'index.json',root);archive=base.private_path(folder/'snapshots',root)
    before=json.loads(index.read_text()) if index.exists() else {'history':[],'publication':'blocked'}
    if before.get('publication')!='blocked' or not isinstance(before.get('history'),list):raise base.ImportFailure('Invalid snapshot index; preserved')
    if before.get('current'):
        key=before['current']
        if not isinstance(key,str) or len(key)!=64 or any(c not in '0123456789abcdef' for c in key):raise base.ImportFailure('Invalid snapshot identifier')
        last=base.private_path(archive/(key+'.json'),root)
        if not last.exists() or hashlib.sha256(last.read_bytes()).hexdigest()!=key:raise base.ImportFailure('Previous snapshot corrupted; no update')
    result=importer.run(source,folder/'candidate.json',folder/'import-report.json',allow_version_change=allow_version_change,root=root)
    if not result['written']:return result
    raw=(folder/'candidate.json').read_bytes();key=hashlib.sha256(raw).hexdigest();target=base.private_path(archive/(key+'.json'),root)
    if target.exists() and target.read_bytes()!=raw:raise base.ImportFailure('Immutable snapshot collision')
    if not target.exists():base.atomic(target,raw)
    history=list(before['history'])
    if key not in history:history.append(key)
    current={'current':key,'previous':before.get('current') if key!=before.get('current') else before.get('previous'),'history':history,'publication':'blocked','game_version':result['game_version'],'counts':result['counts'],'changes':result['changes']}
    base.atomic(index,base.encoded(current));return {**result,'snapshot':key,'index':str(index.relative_to(root))}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--allow-version-change',action='store_true');a=p.parse_args();r=stage(a.input,allow_version_change=a.allow_version_change);print(json.dumps(r));raise SystemExit(0 if r['written'] else 1)
