#!/usr/bin/env python3
"""Normalize legally obtained local Assets.zip into a REVIEW CANDIDATE, never publish.

Schema: docs/DATA_SCHEMA.md. Parent scalar replacement and recursive object override
follow the documented default. Field-specific engine merge exceptions are not guessed.
"""
import argparse
import copy
import hashlib
import json
import os
import shutil
import zipfile
from pathlib import Path

KINDS=('ItemId','ResourceTypeId','ItemTag')

def material(v):
    if not isinstance(v,dict):return None
    keys=[k for k in KINDS if isinstance(v.get(k),str) and v[k]]
    q=v.get('Quantity',1)
    if len(keys)!=1 or type(q)!=int or not 0<q<=999999:return None
    out={'kind':keys[0],'id':v[keys[0]],'quantity':q}
    if v.get('Metadata'):out['metadata']=v['Metadata']
    return out

def materials(value):
    if isinstance(value,dict):value=[value]
    if not isinstance(value,list) or not value:return None
    rows=[material(x) for x in value]
    return rows if all(rows) else None

def merge(parent,child):
    """Documented default: child values override, nested maps override recursively."""
    out=copy.deepcopy(parent)
    for k,v in child.items():
        if k=='Parent':continue
        out[k]=merge(out[k],v) if isinstance(v,dict) and isinstance(out.get(k),dict) else copy.deepcopy(v)
    return out

def resolve_all(assets):
    resolved={};failures={}
    def walk(id,stack):
        if id in resolved:return resolved[id]
        if id in stack:raise ValueError('parent_cycle: '+' -> '.join(stack+[id]))
        if len(stack)>100:raise ValueError('parent_depth_limit')
        if id not in assets:raise ValueError('missing_parent: '+id)
        obj=assets[id]['data'];parent=obj.get('Parent')
        if parent is not None and not isinstance(parent,str):raise ValueError('invalid_parent')
        base=walk(parent,stack+[id]) if parent else {}
        resolved[id]=merge(base,obj)
        return resolved[id]
    for id in assets:
        try:walk(id,[])
        except ValueError as exc:failures[id]=str(exc)
    return resolved,failures

def extract(source):
    assets={'Items':{},'Recipes':{}};errors=[];scanned=0;total=0
    with zipfile.ZipFile(source) as archive:
        for info in archive.infolist():
            path=info.filename.replace('\\','/')
            parts=path.split('/')
            if not path.endswith('.json') or 'Item' not in parts:continue
            group=next((k for k in assets if '/Server/Item/'+k+'/' in '/'+path),None)
            if not group:continue
            scanned+=1;total+=info.file_size
            if info.file_size>3_000_000 or total>500_000_000 or scanned>50000:raise ValueError('Archive size limit')
            id=Path(path).stem
            if id in assets[group]:raise ValueError('Duplicate '+group+' ID: '+id)
            try:obj=json.loads(archive.read(info))
            except (ValueError,UnicodeError,RuntimeError):errors.append({'file':path,'reason':'invalid_json'});continue
            if not isinstance(obj,dict):errors.append({'file':path,'reason':'invalid_object'});continue
            assets[group][id]={'data':obj,'file':path}
    resolved={};items=[]
    for group,rows in assets.items():
        resolved[group],bad=resolve_all(rows)
        errors.extend({'file':rows[id]['file'],'reason':reason} for id,reason in bad.items())
    for id,obj in resolved['Items'].items():
        props=obj.get('TranslationProperties') or {}
        items.append({'id':id,'translation_key':props.get('Name') if isinstance(props,dict) else None,
                      'names':{'en':None,'ru':None},'source_file':assets['Items'][id]['file']})
    known={i['id'] for i in items};recipes=[];incomplete=[]
    candidates=[(assets['Recipes'][id]['file'],obj,None) for id,obj in resolved['Recipes'].items()]
    for id,obj in resolved['Items'].items():
        if obj.get('Recipe') is not None:
            if not isinstance(obj['Recipe'],dict):errors.append({'file':assets['Items'][id]['file'],'reason':'invalid_recipe'});continue
            candidates.append((assets['Items'][id]['file']+'#Recipe',obj['Recipe'],id))
    for path,r,implicit in candidates:
        reasons=[]
        if r.get('Parent'):reasons.append('nested_recipe_parent_unsupported')
        ins=materials(r.get('Input'))
        # A malformed explicit output must never fall back to a different field.
        if r.get('Output') is not None:outs=materials(r['Output'])
        elif r.get('PrimaryOutput') is not None:outs=materials(r['PrimaryOutput'])
        elif implicit:outs=materials({'ItemId':implicit,'Quantity':r.get('OutputQuantity',1)})
        else:outs=None
        if not ins or not outs:errors.append({'file':path,'reason':'unresolved_input_or_output'});continue
        benches=r.get('BenchRequirement') or []
        if not isinstance(benches,list) or any(not isinstance(b,dict) or not isinstance(b.get('Id'),str) for b in benches):reasons.append('invalid_bench_requirements')
        refs=sorted({m['id'] for m in ins+outs if m['kind']=='ItemId' and m['id'] not in known})
        if refs:reasons.append('unresolved_item_ids')
        if any(m['kind']!='ItemId' for m in ins+outs):reasons.append('material_choice_required')
        if any(m.get('metadata') for m in ins+outs):reasons.append('material_metadata_unsupported')
        if len(outs)!=1:reasons.append('multiple_outputs')
        row={'id':path,'inputs':ins,'outputs':outs,'primary_output':material(r.get('PrimaryOutput')),
             'bench_requirements':benches,'time_seconds':r.get('TimeSeconds'),'knowledge_required':r.get('KnowledgeRequired'),
             'required_memories_level':r.get('RequiredMemoriesLevel'),'source_file':path,'unresolved_item_ids':refs,
             'calculation_supported':not reasons,'status':'candidate','reasons':reasons}
        recipes.append(row)
        if reasons:incomplete.append({'id':path,'reasons':reasons})
    with open(source,'rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
    return {'schema_version':3,'source':'Hytale Assets.zip','verification':'local-review-candidate; not published',
            'inheritance_policy':'documented default object override; field-specific engine merges unverified',
            'archive_sha256':digest,'json_files_scanned':scanned,'items':items,'item_count':len(items),
            'recipe_count':len(recipes),'recipes':recipes,'incomplete_recipes':incomplete,
            'rejected_count':len(errors),'rejected_examples':errors}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('assets_zip',type=Path)
    ap.add_argument('--output',type=Path,default=Path('.private/assets-candidate.json'))
    ap.add_argument('--game-version',required=True);ap.add_argument('--expected-sha256')
    ap.add_argument('--report',type=Path,default=Path('.private/assets-import-report.json'));a=ap.parse_args()
    if a.assets_zip.resolve()==a.output.resolve() or a.report.resolve() in (a.output.resolve(),a.assets_zip.resolve()):raise SystemExit('Input/output/report paths must differ')
    data=extract(a.assets_zip);data['game_version']=a.game_version
    if a.expected_sha256 and data['archive_sha256']!=a.expected_sha256.lower():raise SystemExit('Archive checksum mismatch; files preserved')
    report={k:v for k,v in data.items() if k not in ('items','recipes')};a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    if data['rejected_count'] or not data['recipe_count']:raise SystemExit('Unresolved/invalid assets; candidate preserved; see report')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    if a.output.exists():shutil.copy2(a.output,a.output.with_suffix('.previous.json'))
    tmp=a.output.with_suffix('.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2));os.replace(tmp,a.output)
    print('Review candidate:',data['recipe_count'],'recipes;',len(data['incomplete_recipes']),'need choices/review. Not published.')

if __name__=='__main__':main()
