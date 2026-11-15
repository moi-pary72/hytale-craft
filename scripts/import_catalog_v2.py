#!/usr/bin/env python3
"""Offline canonical-v2 review importer. No network, game extraction or publication."""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
try:
    import import_catalog as base
except ModuleNotFoundError:
    from scripts import import_catalog as base

VERSION = 2
SECTIONS = ('sources','items','groups','stations','recipes')


def validate(data):
    errors, warnings, capabilities = [], [], {}
    def error(path, message): errors.append({'path':path,'message':message})
    def integer(v, low=1): return type(v) is int and low <= v <= 999999
    def text(v): return isinstance(v,str) and 0 < len(v.strip()) <= 500
    if not isinstance(data,dict) or set(data) != {'schema_version','snapshot',*SECTIONS} or type(data.get('schema_version')) is not int or data['schema_version'] != VERSION:
        return [{'path':'$','message':'Expected canonical schema_version2 and exact root fields'}],warnings,capabilities
    tables={}
    for section in SECTIONS:
        rows=data[section]
        if not isinstance(rows,list) or len(rows)>base.MAX_ROWS or (section in ('items','sources','recipes') and not rows):
            error(section,'Expected bounded list; items/sources/recipes must be nonempty');rows=[]
        index={}
        for pos,row in enumerate(rows):
            path=f'{section}[{pos}]'
            if not isinstance(row,dict) or not isinstance(row.get('id'),str) or not base.ID.fullmatch(row['id']):
                error(path,'Invalid record or original identifier');continue
            if row['id'] in index:error(path,'Duplicate identifier')
            index[row['id']]=row
        tables[section]=index
    if errors:return errors,warnings,capabilities
    # Reuse the established v1 entity/provenance checks without inventing a recipe.
    common={k:copy.deepcopy(data[k]) for k in ('snapshot','sources','items','stations')}
    common.update(schema_version=1,recipes=[])
    common_errors,common_warnings=base.validate(common)
    errors.extend(e for e in common_errors if not (e['path']=='recipes' and e['message'].startswith('Expected bounded list;')))
    warnings.extend(common_warnings)
    if errors:return errors,warnings,capabilities
    def provenance(row,path):
        if row.get('source_id') not in tables['sources']:error(path,'Unknown source reference')
        if not text(row.get('source_record')):error(path,'Source locator required')
        if row.get('status') not in base.STATES:error(path,'Invalid declared verification state')
        if row.get('game_version',data['snapshot'].get('game_version')) != data['snapshot'].get('game_version'):error(path,'Mixed game versions')
        if row.get('channel',data['snapshot'].get('channel')) != data['snapshot'].get('channel'):error(path,'Mixed game channels')
    for section in ('items','stations'):
        for key,row in tables[section].items():provenance(row,section+'.'+key)
    for key,source in tables['sources'].items():
        license=source.get('license',{})
        for permission in ('automated_access','game_ip_use'):
            if license.get(permission,'unknown') not in ('allowed','prohibited','unknown'):error('sources.'+key,'Invalid rights declaration')
            if license.get(permission,'unknown') != 'allowed':warnings.append({'path':'sources.'+key,'message':permission+' unresolved/restricted; no publication permission'})
    for key,group in tables['groups'].items():
        path='groups.'+key;provenance(group,path)
        if group.get('kind') not in ('resource_type','item_tag','explicit'):error(path,'Invalid group kind')
        if group.get('selection') not in ('mixed','single','unknown'):error(path,'Explicit group selection semantics required')
        if type(group.get('membership_complete')) is not bool:error(path,'membership_complete must be boolean')
        members=group.get('members')
        if not isinstance(members,list) or len(members)>5000:error(path,'Bounded member list required');continue
        if group.get('membership_complete') and not members:error(path,'Complete group cannot be empty')
        seen=set()
        for member in members:
            if not isinstance(member,dict) or set(member)!={'item_id','units'}:error(path,'Expected item_id and resource units');continue
            item=member['item_id']
            if not isinstance(item,str) or item not in tables['items']:error(path,'Unknown group item reference');continue
            if item in seen:error(path,'Duplicate group member')
            seen.add(item)
            if not integer(member['units']):error(path,'Positive integer resource units required')
        if not group.get('membership_complete') or group.get('selection')=='unknown':warnings.append({'path':path,'message':'Group membership/selection unresolved; do not substitute materials'})
    graph={key:set() for key in tables['items']};all_graph={key:set() for key in tables['items']};edge_count=0
    for key,recipe in tables['recipes'].items():
        path='recipes.'+key;provenance(recipe,path);flags=[];input_ids=set();output_ids=[]
        if recipe.get('kind') not in ('craft','processing','salvage','unknown'):error(path,'Invalid transformation kind')
        if recipe.get('kind') in ('salvage','unknown'):flags.append(recipe['kind'])
        inputs=recipe.get('inputs')
        if not isinstance(inputs,list) or not 0<len(inputs)<=100:error(path,'Nonempty bounded input list required');inputs=[]
        signatures=set()
        for slot in inputs:
            if not isinstance(slot,dict) or set(slot)!={'quantity','options'}:error(path,'Input slot requires quantity/options');continue
            if not integer(slot['quantity']):error(path,'Positive integer input quantity required')
            options=slot['options']
            if not isinstance(options,list) or not 0<len(options)<=50:error(path,'Bounded alternative options required');continue
            if len(options)>1:flags.append('alternative_input')
            seen=set()
            for option in options:
                if not isinstance(option,dict) or set(option)!={'kind','id'} or option['kind'] not in ('item','group') or not isinstance(option['id'],str):error(path,'Invalid material selector');continue
                signature=(option['kind'],option['id'])
                if signature in seen:error(path,'Duplicate input option')
                seen.add(signature)
                table=tables['items' if option['kind']=='item' else 'groups']
                if option['id'] not in table:error(path,'Unknown material/group reference');continue
                if option['kind']=='item':input_ids.add(option['id'])
                else:
                    flags.append('resource_group')
                    for member in table[option['id']].get('members',[]):
                        if isinstance(member,dict) and isinstance(member.get('item_id'),str) and member['item_id'] in tables['items']:input_ids.add(member['item_id'])
                edge_count+=len(input_ids)
                if edge_count>100000:return errors+[{'path':path,'message':'Dependency expansion budget exceeded'}],warnings,capabilities
            sig=tuple(sorted(seen))
            if sig in signatures:error(path,'Duplicate input slot; normalize explicitly')
            signatures.add(sig)
        outputs=recipe.get('outputs')
        if not isinstance(outputs,list) or not 0<len(outputs)<=100:error(path,'Nonempty bounded output list required');outputs=[]
        for term in outputs:
            if not isinstance(term,dict) or set(term)!={'item_id','quantity'}:error(path,'Output requires item_id/quantity');continue
            item=term['item_id']
            if not isinstance(item,str) or item not in tables['items']:error(path,'Unknown output item');continue
            if item in output_ids:error(path,'Duplicate output item; normalize explicitly')
            output_ids.append(item)
            if not integer(term['quantity']):error(path,'Positive integer output quantity required')
        if 'primary_output' not in recipe or recipe['primary_output'] is not None and recipe['primary_output'] not in output_ids:error(path,'Primary output must be null or one existing output; never add it twice')
        if len(outputs)>1:flags.append('multiple_outputs')
        requirement=recipe.get('station_requirements')
        if not isinstance(requirement,dict) or set(requirement)!={'mode','entries'} or requirement.get('mode') not in ('any','all','unknown') or not isinstance(requirement.get('entries'),list) or len(requirement['entries'])>50:
            error(path,'Explicit bounded station requirement semantics required');requirement={'mode':'unknown','entries':[]}
        if requirement['entries'] and requirement['mode']=='unknown':flags.append('unknown_station_semantics')
        for entry in requirement['entries']:
            if not isinstance(entry,dict) or set(entry)!={'station_id','type','min_level','categories','augment_tags'}:error(path,'Invalid station entry');continue
            if not isinstance(entry['station_id'],str) or entry['station_id'] not in tables['stations']:error(path,'Unknown station')
            if entry['type'] not in ('Crafting','Processing','DiagramCrafting','StructuralCrafting','unknown'):error(path,'Invalid station type')
            if entry['min_level'] is not None and not integer(entry['min_level'],0):error(path,'Invalid station level')
            for field in ('categories','augment_tags'):
                if not isinstance(entry[field],list) or len(entry[field])>50 or not all(text(v) for v in entry[field]):error(path,'Invalid station '+field)
        unlock=recipe.get('requirements')
        if not isinstance(unlock,dict) or set(unlock)!={'knowledge_required','memories_level'}:error(path,'Explicit unlock fields required')
        else:
            if unlock['knowledge_required'] is not None and type(unlock['knowledge_required']) is not bool:error(path,'Invalid knowledge flag')
            if unlock['memories_level'] is not None and not integer(unlock['memories_level']):error(path,'Invalid memories level')
        seconds=recipe.get('time_seconds')
        if seconds is not None and (type(seconds) not in (int,float) or not math.isfinite(seconds) or not 0<=seconds<=999999):error(path,'Invalid crafting time')
        capabilities[key]={'legacy_arithmetic_shape':not flags,'unsupported_features':sorted(set(flags))}
        edge_count+=len(output_ids)*len(input_ids)
        if edge_count>100000:return errors+[{'path':path,'message':'Dependency expansion budget exceeded'}],warnings,capabilities
        for output in output_ids:
            all_graph[output].update(input_ids)
            if recipe.get('kind') in ('craft','processing'):graph[output].update(input_ids)
    for label,g in [('craft_processing',graph),('all_transformations',all_graph)]:
        cycles=cycle_paths(g)
        if cycles:
            warnings.append({'path':'recipes','message':'Conservative '+label+' cycle candidates; explicit route selection required','paths':cycles})
            if label=='craft_processing':
                for c in capabilities.values():c['legacy_arithmetic_shape']=False;c['unsupported_features']=sorted(set(c['unsupported_features']+['cycle_candidate']))
    return errors,warnings,capabilities


def cycle_paths(graph):
    color={};found=[]
    for start in sorted(graph):
        if color.get(start):continue
        color[start]=1;path=[start];active={start:0};stack=[(start,iter(sorted(graph[start])))]
        while stack:
            node,edges=stack[-1];target=next(edges,None)
            if target is None:color[node]=2;stack.pop();active.pop(node);path.pop();continue
            if color.get(target)==1:
                if len(found)<20:found.append(path[active[target]:]+[target])
            elif not color.get(target):
                if len(path)>=256:raise base.ImportFailure('Dependency depth exceeds256')
                color[target]=1;active[target]=len(path);path.append(target);stack.append((target,iter(sorted(graph[target]))))
    return found


def diff(previous,current):
    result={}
    for section in SECTIONS:
        old={r['id']:r for r in previous.get(section,[])};new={r['id']:r for r in current[section]}
        result[section]={'added':sorted(new.keys()-old.keys()),'removed':sorted(old.keys()-new.keys()),'changed':sorted(k for k in old.keys()&new.keys() if base.encoded(old[k])!=base.encoded(new[k]))}
    return result


def run(source,output=Path('.private/catalog-v2-candidate.json'),report=Path('.private/catalog-v2-report.json'),allow_version_change=False,root=base.ROOT,expected_sha256=None):
    output,report=base.private_path(output,root),base.private_path(report,root);source=Path(source)
    if len({source.resolve(),output.resolve(),report.resolve()})!=3:raise base.ImportFailure('Input/output/report must differ')
    result={'importer_version':VERSION,'publication':'blocked-pending-owner-and-rights-review','errors':[],'warnings':[],'written':False}
    try:
        with source.open('rb') as f:raw=f.read(base.MAX_BYTES+1)
        if len(raw)>base.MAX_BYTES:raise base.ImportFailure('Input exceeds10MB')
        digest=hashlib.sha256(raw).hexdigest()
        if expected_sha256 is not None and (not isinstance(expected_sha256,str) or digest!=expected_sha256.lower()):raise base.ImportFailure('Input SHA-256 mismatch')
        data=base.strict_json(raw);errors,warnings,capabilities=validate(data);result.update(errors=errors,warnings=warnings,input_sha256=digest)
        if errors:return result
        previous={}
        if output.exists():
            old=output.read_bytes();previous=base.strict_json(old)
            if not isinstance(previous,dict) or previous.get('schema_version')!=VERSION:raise base.ImportFailure('Existing candidate schema invalid; preserve prior bytes')
            cleaned={k:v for k,v in previous.items() if k in ('schema_version','snapshot',*SECTIONS)}
            if validate(cleaned)[0]:raise base.ImportFailure('Existing candidate invalid; preserve prior bytes')
            if any(previous['snapshot'][k]!=data['snapshot'][k] for k in ('game_version','channel')) and not allow_version_change:raise base.ImportFailure('Version/channel change requires --allow-version-change')
        result['changes']=diff(previous,data)
        result['snapshot_change']={'before':previous.get('snapshot'),'after':copy.deepcopy(data['snapshot'])}
        candidate=copy.deepcopy(data);candidate['publication']={'status':'blocked','approval_required':True,'reason':'No importer flag or source declaration authorizes publication'}
        candidate['import_provenance']={'importer_version':VERSION,'input_sha256':digest,'input_name':source.name};candidate['calculation_capabilities']=capabilities
        candidate['record_sha256']={section:{r['id']:hashlib.sha256(base.encoded(r)).hexdigest() for r in data[section]} for section in SECTIONS}
        payload=base.encoded(candidate)
        if output.exists() and old!=payload:
            backup=output.with_name(output.name+'.'+hashlib.sha256(old).hexdigest()+'.previous')
            if backup.exists() and backup.read_bytes()!=old:raise base.ImportFailure('Backup collision')
            if not backup.exists():base.atomic(backup,old)
            result['backup']=backup.name
        base.atomic(output,payload);result.update(written=True,candidate_sha256=hashlib.sha256(payload).hexdigest(),game_version=data['snapshot']['game_version'],counts={s:len(data[s]) for s in SECTIONS})
    except (ValueError,OSError,TypeError,UnicodeError,RecursionError,KeyError) as e:result['errors'].append({'path':'$','message':str(e)[:500]})
    finally:base.atomic(report,base.encoded(result))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--output',type=Path,default=Path('.private/catalog-v2-candidate.json'));p.add_argument('--report',type=Path,default=Path('.private/catalog-v2-report.json'));p.add_argument('--allow-version-change',action='store_true');p.add_argument('--expected-sha256');a=p.parse_args()
    try:r=run(a.input,a.output,a.report,a.allow_version_change,expected_sha256=a.expected_sha256)
    except base.ImportFailure as e:p.exit(2,str(e)+'\n')
    print(json.dumps(r,ensure_ascii=False));return 0 if r['written'] else 1
if __name__=='__main__':raise SystemExit(main())
