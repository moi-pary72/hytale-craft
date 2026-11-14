#!/usr/bin/env python3
"""Export an owner-review offline HTML. Not a deployment or a production build.

Includes the existing non-commercial snapshots; their restrictions still apply.
"""
import argparse
import base64
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def safe_js(data):return json.dumps(data,ensure_ascii=True).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
def export(output):
    source=(ROOT/'preview.html').read_text()
    manifest=json.loads((ROOT/'data/recipes/manifest.json').read_text())
    raw=(ROOT/'data/recipes'/manifest['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=manifest['sha256']:raise ValueError('Recipe snapshot checksum mismatch')
    paths=['data/recipes/manifest.json','data/recipes/'+manifest['path'],'data/catalog.json']+['locales/'+lang+'.json' for lang in ('en','ru','es','pt-BR')]
    data={p:(ROOT/p).read_text() for p in paths}
    pictures={p.stem:'data:image/svg+xml;base64,'+base64.b64encode(p.read_bytes()).decode() for p in (ROOT/'assets/preview').glob('*.svg')}
    bootstrap='<script>window.CRAFT_OFFLINE_DATA='+safe_js(data)+';window.CRAFT_OFFLINE_IMAGES='+safe_js(pictures)+';window.fetch=async function(url){const key=String(url);if(Object.hasOwn(CRAFT_OFFLINE_DATA,key))return new Response(CRAFT_OFFLINE_DATA[key],{status:200,headers:{"Content-Type":"application/json"}});throw Error("Offline resource unavailable");};</script>'
    source=source.replace('<link rel="stylesheet" href="web/preview/style.css">','<style>'+(ROOT/'web/preview/style.css').read_text()+'</style>')
    scripts=[]
    for path in re.findall(r'<script defer src="([^"]+)"></script>',source):
        code=(ROOT/path).read_text().replace("'assets/preview/'+id+'.svg'",'window.CRAFT_OFFLINE_IMAGES[id]')
        scripts.append('<script>'+code.replace('</script','<\\/script')+'</script>')
    source=re.sub(r'<script defer src="[^"]+"></script>','',source)
    source=source.replace('href="./"','href="https://moi-pary72.github.io/hytale-craft/"')
    source=source.replace('</body>',bootstrap+''.join(scripts)+'</body>')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(source)
    return output
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='.private/hytale-craft-preview.html');args=parser.parse_args();path=export(args.output);print('Offline non-commercial review artifact:',path,'bytes:',path.stat().st_size)
