#!/usr/bin/env python3
"""Import the documented non-commercial HySphere export; unresolved rows stay separate.

No HTML scraping. No invented group members. Does not mark third-party data official.
"""
import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from datetime import datetime

ORIGIN = 'https://hysphere.app'
LICENSE = ORIGIN + '/about#data-license'

def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)+'\n').encode()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def fetch(path):
    # The documented export accepts curl; urllib's default UA is denied upstream.
    result = subprocess.run(['curl','--fail','--silent','--show-error','--proto','=https',
                             '--max-time','45','--max-filesize','15000000',ORIGIN+path],capture_output=True,check=True)
    if len(result.stdout)>15_000_000:raise ValueError('Oversized export')
    return result.stdout

def normalize(manifest, item_data, recipe_data, hashes):
    if manifest.get('contract')!='sphere-data/v1' or manifest.get('license',{}).get('url')!=LICENSE:
        raise ValueError('Contract/license changed; manual review required')
    date=manifest.get('extractedAt','')
    if not isinstance(date,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:T[0-9:.]+Z)?',date):raise ValueError('Invalid extraction date')
    datetime.fromisoformat(date.replace('Z','+00:00'))
    for data,key in ((item_data,'items'),(recipe_data,'recipes')):
        if data.get('contract')!='sphere-data/v1' or data.get('extractedAt')!=manifest.get('extractedAt') or data.get('gameVersion')!=manifest.get('game',{}).get('version'):
            raise ValueError('Mixed export revisions/game versions')
        rows=data.get(key)
        count=next(x['recordCount'] for x in manifest['datasets'] if x['id']==key)
        if not isinstance(rows,list) or not rows or len(rows)!=data.get('count') or len(rows)!=count:
            raise ValueError('Empty or truncated export')
        ids=[x.get('id') for x in rows]
        if any(not isinstance(i,str) or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,200}',i) for i in ids) or len(set(ids))!=len(ids):
            raise ValueError('Invalid or duplicate IDs')
    items=[]
    category_map={'Weapon':'weapons','Armor':'armor','Tool':'tools','Food':'food','Bench':'benches','Furniture':'decor','Plant':'farming','Rock':'building','Wood':'building','Build':'building'}
    for item in item_data['items']:
        category=category_map.get(item.get('category'),category_map.get(item['id'].split('_')[0],'other'))
        items.append({'id':item['id'],'names':{'en':item.get('name') or None,'ru':None},'category':category})
    known={x['id'] for x in items};recipes=[];incomplete=[]
    for row in recipe_data['recipes']:
        issues=[]
        def materials(key):
            rows=row.get(key)
            if not isinstance(rows,list) or not rows:issues.append('missing_'+key);return []
            out=[]
            for v in rows:
                if not isinstance(v,dict) or v.get('itemId') not in known or type(v.get('quantity'))!=int or not 0<v['quantity']<=999999:
                    issues.append('unresolved_'+key);continue
                out.append({'kind':'ItemId','id':v['itemId'],'quantity':v['quantity']})
            return out
        inputs=materials('inputs');outputs=materials('outputs')
        if row.get('kind')!='craft':issues.append('salvage_not_auto_crafted')
        if len(outputs)!=1:issues.append('multiple_or_missing_outputs')
        benches=row.get('benches')
        if not isinstance(benches,list) or any(not isinstance(b,dict) or not b.get('id') or b['id'].upper() in ('TODO','UNKNOWN') or (b.get('tier') is not None and (type(b['tier'])!=int or b['tier']<0)) for b in benches or []):
            issues.append('unresolved_station')
        if any(v.get('resourceTypeId') or v.get('itemTag') for v in row.get('inputs',[]) if isinstance(v,dict)):
            issues.append('unresolved_material_group')
        if issues:
            incomplete.append({'id':row['id'],'outputs':[v.get('itemId') for v in row.get('outputs',[]) if isinstance(v,dict) and v.get('itemId')], 'reasons':sorted(set(issues))})
        else:
            recipes.append({'id':row['id'],'inputs':inputs,'outputs':outputs,'bench_requirements':benches,
                            'knowledge_required':row.get('knowledgeRequired'), 'time_seconds':row.get('timeSeconds'),
                            'status':'source-backed','source_url':ORIGIN+'/data/v1/recipes.json'})
    if not recipes:raise ValueError('No complete recipes; working snapshot preserved')
    return {'schema_version':3,'source':{'name':'HySphere','url':ORIGIN+'/data','license_url':LICENSE,'usage':'non-commercial-attribution',
            'extracted_at':manifest['extractedAt'],'revision':manifest['revision'],'game_version':manifest['game']['version'],
            'exact_build':None,'verification':'community-extracted; structurally validated; not official verification','raw_sha256':hashes},
            'items':sorted(items,key=lambda x:x['id']),'recipes':sorted(recipes,key=lambda x:x['id']),
            'incomplete_recipes':sorted(incomplete,key=lambda x:x['id'])}

def write_snapshot(data, root=Path('data/recipes')):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    slug='hysphere-'+data['source']['extracted_at'][:10]
    dest=root/(slug+'.json');raw=encoded(data)
    if dest.exists():
        old=json.loads(dest.read_text())
        if len(data['recipes'])<len(old['recipes'])*.8 or len(data['items'])<len(old['items'])*.8:
            raise ValueError('Snapshot shrank by >20%; manual review required')
        if dest.read_bytes()==raw:return False
        dest.with_suffix('.previous.json').write_bytes(dest.read_bytes())
    tmp=dest.with_suffix('.tmp');tmp.write_bytes(raw);tmp.replace(dest)
    pointer={'schema_version':1,'active':slug,'path':dest.name,'sha256':sha(raw)}
    target=root/'manifest.json'
    if target.exists():target.with_suffix('.previous.json').write_bytes(target.read_bytes())
    tmp=target.with_suffix('.tmp');tmp.write_bytes(encoded(pointer));tmp.replace(target)
    return True

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--local-dir',type=Path);args=ap.parse_args()
    report={'status':'failed','publication':'source-backed recipes only; no official verification'}
    try:
        raw={key:((args.local_dir/('hysphere-'+key+'.json')).read_bytes() if args.local_dir else fetch('/data/v1/'+key+'.json')) for key in ('manifest','items','recipes')}
        data=normalize(*(json.loads(raw[k]) for k in ('manifest','items','recipes')),{k:sha(v) for k,v in raw.items()})
        changed=write_snapshot(data)
        report={'status':'validated','items':len(data['items']),'source_backed_recipes':len(data['recipes']),'incomplete_recipes':len(data['incomplete_recipes']),
                'reasons':dict(Counter(reason for r in data['incomplete_recipes'] for reason in r['reasons'])),'source':data['source']}
        print(json.dumps({'changed':changed,**report},ensure_ascii=False))
    except Exception as exc:
        report['error']=str(exc)[:500]
        raise
    finally:
        Path('docs/reports').mkdir(exist_ok=True,parents=True)
        Path('docs/reports/recipe-sync.json').write_bytes(encoded(report))

if __name__=='__main__':main()
