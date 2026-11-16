#!/usr/bin/env python3
"""Standalone UI-only beta owner preview; no deploy and no community data."""
import argparse,base64,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def safe(value):return json.dumps(value,ensure_ascii=True).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
def export(output):
    html=(ROOT/'beta.html').read_text()
    data={f'locales/{prefix}{lang}.json':(ROOT/'locales'/prefix/f'{lang}.json').read_text() for prefix in ('','beta/') for lang in ('en','ru','es','pt-BR')}
    images={('item-'+p.stem if directory=='assets/learning-items' else p.stem):'data:image/webp;base64,'+base64.b64encode(p.read_bytes()).decode() for directory in ('assets/art-pair','assets/ui-v2','assets/learning-items','assets/item-system') for p in (ROOT/directory).glob('*.webp')}
    import importlib.util
    spec=importlib.util.spec_from_file_location('canonical_publication',ROOT/'scripts/canonical_publication.py');gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    _,approval,raw=gate.approved_learning(ROOT);data['web/beta/advanced-data.json']=raw.decode()
    bootstrap='<script>window.CRAFT_BUILD='+safe({'canonicalApproval':approval})+';window.CRAFT_BETA_IMAGES='+safe(images)+';const dictionaries='+safe(data)+';window.fetch=async url=>{if(Object.hasOwn(dictionaries,String(url)))return new Response(dictionaries[String(url)],{status:200});throw Error("No game database in beta");};</script>'
    for path in re.findall(r'<link rel="stylesheet" href="([^"]+)">',html):html=html.replace('<link rel="stylesheet" href="'+path+'">','<style>'+(ROOT/path).read_text()+'</style>')
    # Embed both markup resources and stylesheet-relative artwork for a true single-file preview.
    for directory in ('assets/art-pair','assets/ui-v2','assets/learning-items','assets/item-system'):
        for path in (ROOT/directory).glob('*.webp'):
            uri=images[('item-'+path.stem if directory=='assets/learning-items' else path.stem)]
            html=html.replace('../../'+directory+'/'+path.name,uri).replace('../'+directory+'/'+path.name,uri).replace(directory+'/'+path.name,uri)
    scripts=['<script>'+(ROOT/path).read_text().replace('</script','<\\/script')+'</script>' for path in re.findall(r'<script defer src="([^"]+)"></script>',html)]
    html=re.sub(r'<script defer src="[^"]+"></script>','',html).replace('</body>',bootstrap+''.join(scripts)+'</body>')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(html);return output
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='.private/stage6/hytale-craft-beta.html');a=p.parse_args();out=export(a.output);print(out,out.stat().st_size)
