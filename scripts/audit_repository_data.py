#!/usr/bin/env python3
"""Check tracked files, not history: prevent known dataset reintroduction.

Heuristic guard, not copyright detection or a licence opinion. IDs/links/counts alone
are not declared infringing. History/other refs require a separate audit.
"""
import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def audit(root=ROOT):
    paths=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0');issues=[]
    for name in filter(None,paths):
        p=root/name
        if not p.is_file():continue
        if name.startswith('.private/') or name.endswith(('.zip','.previous.json')):issues.append(name+': private/archive material tracked')
        if name.startswith('data/recipes/') and name.endswith('.json') and name!='data/recipes/manifest.json':issues.append(name+': game snapshot path withheld')
        if not name.endswith('.json'):continue
        data=json.loads(p.read_text())
        if name=='data/catalog.json' and any(data.get(k) for k in ('items','recipes','recipe_ids')):issues.append(name+': neutral catalogue must stay empty')
        if name=='data/recipes/manifest.json' and any(data.get(k) for k in ('path','active','sha256')):issues.append(name+': neutral manifest must not select a snapshot')
        def walk(obj):
            if isinstance(obj,dict):
                if 'import_provenance' in obj and 'publication' in obj:issues.append(name+': review candidate must remain private')
                for k,v in obj.items():
                    if k in ('items','recipes') and isinstance(v,list) and len(v)>20:issues.append(name+': bulk dataset requires explicit publication review')
                    walk(v)
            elif isinstance(obj,list):
                for v in obj:walk(v)
        walk(data)
    if issues:raise ValueError('\n'.join(sorted(set(issues))))
    return {'tracked_files_checked':len(list(filter(None,paths))),'known_dataset_reintroduction':False,'scope':'current tracked tree only; not legal clearance'}
if __name__=='__main__':print(json.dumps(audit(),indent=2))
