#!/usr/bin/env python3
"""Generate an isolated, user-only art review. Does not alter Pages output."""
import argparse
import base64
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def create(offline=False):
    html=(ROOT/'preview.html').read_text()
    html=re.sub(r'<link rel="canonical"[^>]*>','',html)
    html=html.replace('<script defer src="web/preview/i18n.js">','<link rel="stylesheet" href="web/art-pair/style.css"><script defer src="web/art-pair/config.js"></script><script defer src="web/art-pair/cards.js"></script><script defer src="web/preview/i18n.js">')
    html=html.replace('href="./" data-i18n="legacy"','href="#goals" data-i18n="home"')
    html=html.replace('The current planner is available at the site root.','Enable JavaScript to review the cards.')
    if not offline:return html
    import json
    def safe(value):return json.dumps(value,ensure_ascii=True).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    images={p.stem:'data:image/webp;base64,'+base64.b64encode(p.read_bytes()).decode() for p in (ROOT/'assets/art-pair').glob('*.webp')}
    data={'locales/'+lang+'.json':(ROOT/'locales'/f'{lang}.json').read_text() for lang in ('en','ru','es','pt-BR')}
    bootstrap='<script>window.CRAFT_ART_IMAGES='+safe(images)+';window.CRAFT_ART_LOCALES='+safe(data)+';window.fetch=async function(url){if(Object.hasOwn(CRAFT_ART_LOCALES,String(url)))return new Response(CRAFT_ART_LOCALES[String(url)],{status:200});throw Error("No game dataset in art review");};</script>'
    for path in re.findall(r'<link rel="stylesheet" href="([^"]+)">',html):
        html=html.replace('<link rel="stylesheet" href="'+path+'">','<style>'+(ROOT/path).read_text()+'</style>')
    scripts=[]
    for path in re.findall(r'<script defer src="([^"]+)"></script>',html):
        scripts.append('<script>'+(ROOT/path).read_text().replace('</script','<\\/script')+'</script>')
    html=re.sub(r'<script defer src="[^"]+"></script>','',html)
    return html.replace('</body>',bootstrap+''.join(scripts)+'</body>')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--offline',action='store_true');p.add_argument('--output');a=p.parse_args();out=Path(a.output or ('.private/stage5/art-pair-mobile.html' if a.offline else 'art-preview.html'));out.parent.mkdir(parents=True,exist_ok=True);out.write_text(create(a.offline));print(out,out.stat().st_size)
