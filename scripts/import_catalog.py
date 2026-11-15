#!/usr/bin/env python3
"""Offline JSON review importer. No network, game extraction, or publication."""
import argparse
import copy
import hashlib
import json
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
STATES = ('verified', 'unverified', 'tutorial', 'incomplete', 'blocked')
MAX_BYTES = 10_000_000
MAX_ROWS = 10_000
ID = re.compile(r'[A-Za-z0-9_.:-]{1,200}')

class ImportFailure(ValueError):
    pass

def strict_json(raw):
    def pairs(values):
        obj = {}
        for key, value in values:
            if key in obj:
                raise ImportFailure('Duplicate JSON key: ' + key)
            obj[key] = value
        return obj
    def constant(value):
        raise ImportFailure('Non-finite JSON number: ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)

def encoded(data):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()

def validate(data):
    errors, warnings = [], []
    def error(path, message):
        errors.append({'path': path, 'message': message})
    def text(value):
        return isinstance(value, str) and bool(value.strip()) and len(value) <= 500
    def https(value):
        if not text(value): return False
        u = urlsplit(value)
        return u.scheme == 'https' and bool(u.hostname) and not u.username and not u.password
    if not isinstance(data, dict):
        return [{'path':'$', 'message':'Expected JSON object'}], warnings
    expected = {'schema_version','snapshot','sources','items','stations','recipes'}
    if set(data) != expected or type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        error('$', 'Unsupported schema or unexpected/missing top-level fields')
    snapshot = data.get('snapshot')
    if not isinstance(snapshot, dict): snapshot = {}; error('snapshot', 'Expected object')
    for key in ('game_version','channel','source_revision','updated_at'):
        if not text(snapshot.get(key)): error('snapshot.'+key, 'Required bounded version/provenance string')
    try:
        stamp = datetime.fromisoformat(str(snapshot.get('updated_at','')).replace('Z','+00:00'))
        if stamp.tzinfo is None: raise ValueError()
    except ValueError: error('snapshot.updated_at', 'Expected timezone-aware ISO timestamp')
    tables = {}
    for section in ('sources','items','stations','recipes'):
        rows = data.get(section)
        if not isinstance(rows, list) or len(rows)>MAX_ROWS or (section!='stations' and not rows):
            error(section, 'Expected bounded list; sources/items/recipes must be nonempty'); rows=[]
        index = {}
        for pos, row in enumerate(rows):
            path = f'{section}[{pos}]'
            if not isinstance(row, dict): error(path, 'Expected object'); continue
            key = row.get('id')
            if not isinstance(key,str) or not ID.fullmatch(key): error(path+'.id','Invalid original identifier'); continue
            if key in index: error(path+'.id','Duplicate identifier: '+key)
            index[key] = row
        tables[section] = index
    for key, source in tables['sources'].items():
        path='sources.'+key
        if not https(source.get('url')): error(path+'.url','Expected HTTPS source URL without credentials')
        if not text(source.get('revision')): error(path+'.revision','Source revision required')
        license = source.get('license')
        if not isinstance(license,dict): error(path+'.license','Explicit licence metadata required'); continue
        if not text(license.get('id')) or not https(license.get('url')): error(path+'.license','Licence ID and HTTPS URL required')
        for permission in ('commercial_use','redistribution'):
            if license.get(permission) not in ('allowed','prohibited','unknown'): error(path+'.license.'+permission,'Use allowed/prohibited/unknown')
        # These are declarations, never a legal approval or automatic publishing switch.
        if any(license.get(p)!='allowed' for p in ('commercial_use','redistribution')):
            warnings.append({'path':path,'message':'Rights unknown/restricted; blocked from publication'})
    for section in ('items','stations','recipes'):
        for key,row in tables[section].items():
            path=section+'.'+key
            if row.get('source_id') not in tables['sources']: error(path+'.source_id','Unknown source reference')
            if row.get('status') not in STATES: error(path+'.status','Unknown verification state')
            if row.get('game_version',snapshot.get('game_version')) != snapshot.get('game_version'): error(path+'.game_version','Mixed game versions')
            if not text(row.get('source_record')): error(path+'.source_record','Source record/path required')
            if section in ('items','stations'):
                names=row.get('names')
                if not isinstance(names,dict) or not names or any(not isinstance(lang,str) or not re.fullmatch(r'[a-z]{2}(?:-[A-Za-z]{2,4})?',lang) or (value is not None and not text(value)) for lang,value in names.items()): error(path+'.names','Expected language map with strings/null')
            if section=='items' and not text(row.get('category')): error(path+'.category','Category required; use explicit unknown when unknown')
    graph={key:set() for key in tables['items']}
    for key,recipe in tables['recipes'].items():
        path='recipes.'+key; refs={}
        for field in ('inputs','outputs'):
            rows=recipe.get(field)
            if not isinstance(rows,list) or not rows or len(rows)>100: error(path+'.'+field,'Nonempty material list required'); rows=[]
            seen=set(); refs[field]=[]
            for i,term in enumerate(rows):
                loc=path+'.'+field+f'[{i}]'
                if not isinstance(term,dict) or set(term)!={'item_id','quantity'}: error(loc,'Expected item_id and quantity only'); continue
                item=term['item_id'];q=term['quantity']
                if not isinstance(item,str) or item not in tables['items']: error(loc+'.item_id','Unknown item reference'); continue
                if item in seen: error(loc+'.item_id','Duplicate material; combine quantities explicitly')
                seen.add(item)
                if type(q) is not int or not 0<q<=999999: error(loc+'.quantity','Expected positive bounded integer')
                refs[field].append(item)
        stations=recipe.get('stations')
        if not isinstance(stations,list): error(path+'.stations','Explicit station list required'); stations=[]
        seen=set()
        for station in stations:
            if not isinstance(station,str) or station not in tables['stations']: error(path+'.stations','Unknown station reference'); continue
            if station in seen: error(path+'.stations','Duplicate station')
            seen.add(station)
        for output in refs['outputs']: graph[output].update(refs['inputs'])
        if len(refs['outputs'])>1: warnings.append({'path':path,'message':'Multiple outputs preserved; current public planner support not asserted'})
        if recipe.get('status')=='incomplete': warnings.append({'path':path,'message':'Incomplete declaration preserved, not promoted'})
    # Iterative DFS avoids Python recursion failure. Union of alternatives is conservative.
    color={};cycle_paths=[]
    for start in sorted(graph):
        if color.get(start): continue
        color[start]=1;path=[start];active={start:0};stack=[(start,iter(sorted(graph[start])))]
        while stack:
            node,edges=stack[-1]
            target=next(edges,None)
            if target is None:
                color[node]=2;stack.pop();active.pop(node);path.pop();continue
            if color.get(target)==1:
                cycle=path[active[target]:]+[target]
                if len(cycle_paths)<20: cycle_paths.append(cycle)
                continue
            if not color.get(target):
                if len(path)>=256:
                    error('recipes','Dependency depth exceeds256');return errors,warnings
                color[target]=1;active[target]=len(path);path.append(target);stack.append((target,iter(sorted(graph[target]))))
    for cycle in cycle_paths: error('recipes','Recipe cycle: '+' -> '.join(cycle))
    return errors,warnings

def private_path(path, root):
    private=root/'.private'
    if private.is_symlink(): raise ImportFailure('.private must not be a symlink')
    path=Path(path)
    if not path.is_absolute(): path=root/path
    if not path.resolve().is_relative_to(private.resolve()): raise ImportFailure('Outputs must remain inside .private; no public writes')
    if path.is_symlink(): raise ImportFailure('Symlink output forbidden')
    return path

def atomic(path, raw):
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.import-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f: f.write(raw)
        os.replace(name,path)
    finally:
        if os.path.exists(name): os.unlink(name)

def run(source, output=Path('.private/catalog-candidate.json'), report=Path('.private/catalog-import-report.json'), allow_version_change=False, root=ROOT, expected_sha256=None):
    output,report=private_path(output,root),private_path(report,root)
    source=Path(source)
    if len({source.resolve(),output.resolve(),report.resolve()})!=3: raise ImportFailure('Input/output/report must differ')
    result={'schema_version':1,'candidate_only':True,'publication':'blocked-pending-owner-and-rights-review','errors':[],'warnings':[],'written':False}
    try:
        with source.open('rb') as f: raw=f.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES: raise ImportFailure('Input exceeds10MB')
        if expected_sha256 is not None and (not re.fullmatch(r'[a-fA-F0-9]{64}',expected_sha256) or hashlib.sha256(raw).hexdigest()!=expected_sha256.lower()): raise ImportFailure('Input SHA-256 mismatch; prior candidate preserved')
        data=strict_json(raw);errors,warnings=validate(data);result.update(errors=errors,warnings=warnings,input_sha256=hashlib.sha256(raw).hexdigest())
        if errors: return result
        if output.exists():
            old=output.read_bytes();previous=strict_json(old)
            if not isinstance(previous,dict) or not isinstance(previous.get('snapshot'),dict) or not isinstance(previous['snapshot'].get('game_version'),str) or not previous['snapshot']['game_version'].strip():
                raise ImportFailure('Existing candidate metadata invalid; prior candidate preserved')
            if previous.get('snapshot',{}).get('game_version')!=data['snapshot']['game_version'] and not allow_version_change: raise ImportFailure('Version change requires --allow-version-change; prior candidate preserved')
        candidate=copy.deepcopy(data)
        candidate['import_provenance']={'importer_version':1,'input_sha256':result['input_sha256'],'input_name':source.name}
        candidate['publication']={'status':'blocked','approval_required':True}
        candidate['declared_state_counts']={s:sum(r['status']==s for section in ('items','stations','recipes') for r in data[section]) for s in STATES}
        payload=encoded(candidate)
        if output.exists() and old!=payload:
            digest=hashlib.sha256(old).hexdigest();backup=output.with_name(output.name+'.'+digest+'.previous')
            if backup.exists() and backup.read_bytes()!=old: raise ImportFailure('Backup collision; refusing overwrite')
            if not backup.exists(): atomic(backup,old)
            result['backup']=backup.name
        atomic(output,payload);result.update(written=True,candidate_sha256=hashlib.sha256(payload).hexdigest(),items=len(data['items']),recipes=len(data['recipes']),game_version=data['snapshot']['game_version'])
    except (ValueError,OSError,TypeError,UnicodeError,RecursionError) as exc:
        result['errors'].append({'path':'$','message':str(exc)[:500]})
    finally: atomic(report,encoded(result))
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--output',type=Path,default=Path('.private/catalog-candidate.json'));p.add_argument('--report',type=Path,default=Path('.private/catalog-import-report.json'));p.add_argument('--allow-version-change',action='store_true');p.add_argument('--expected-sha256');a=p.parse_args()
    try: result=run(a.input,a.output,a.report,a.allow_version_change,expected_sha256=a.expected_sha256)
    except ImportFailure as e: p.exit(2,str(e)+'\n')
    print(json.dumps(result,ensure_ascii=False));return 0 if result['written'] else 1

if __name__=='__main__': raise SystemExit(main())
