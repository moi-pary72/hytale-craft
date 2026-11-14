#!/usr/bin/env python3
"""Prepare a static, noindex review build. Never deploys or downloads anything."""
import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ('en', 'ru', 'es', 'pt-BR')

def build(policy='user-only', site_url=None):
    if policy not in ('user-only', 'noncommercial-review'):
        raise ValueError('Unknown data policy')
    if site_url:
        u = urlsplit(site_url)
        if u.scheme != 'https' or not u.hostname or u.username or u.password or u.query or u.fragment or u.path not in ('', '/'):
            raise ValueError('SITE_URL must be an HTTPS origin without credentials, query or path')
        site_url = site_url.rstrip('/')
    (ROOT/'.private').mkdir(exist_ok=True)
    target = ROOT / 'dist'
    if target.is_symlink():
        raise ValueError('dist must not be a symlink')
    with tempfile.TemporaryDirectory(prefix='pages-', dir=ROOT / '.private') as tmp:
        out = Path(tmp)
        paths = ['web/planner.js', 'web/game-recipes.js', 'web/preview/app.js',
                 'web/preview/i18n.js', 'web/preview/style.css']
        paths += ['locales/' + lang + '.json' for lang in LANGUAGES]
        paths += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'assets/preview').glob('*.svg'))]
        if policy == 'noncommercial-review':
            manifest = json.loads((ROOT/'data/recipes/manifest.json').read_text())
            name = manifest['path']
            if Path(name).name != name or not name.endswith('.json'):
                raise ValueError('Unsafe snapshot path')
            snapshot = ROOT/'data/recipes'/name
            if hashlib.sha256(snapshot.read_bytes()).hexdigest() != manifest['sha256']:
                raise ValueError('Recipe snapshot checksum mismatch')
            data = json.loads(snapshot.read_text())
            catalog = json.loads((ROOT/'data/catalog.json').read_text())
            if not data.get('items') or not data.get('recipes') or not catalog.get('items'):
                raise ValueError('Empty community database')
            paths += ['data/catalog.json', 'data/recipes/manifest.json', 'data/recipes/'+name]
        for name in paths:
            src = ROOT/name
            if src.is_symlink():
                raise ValueError('Symlink input forbidden')
            dest = out/name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)
        config = {'testing': True, 'dataPolicy': 'user-only' if policy == 'user-only' else 'community', 'requestTimeoutMs': 12000}
        (out/'web/build-config.js').write_text('window.CRAFT_BUILD='+json.dumps(config)+';\n')
        html = (ROOT/'preview.html').read_text()
        html = html.replace('<script defer src="web/preview/i18n.js">', '<script defer src="web/build-config.js"></script><script defer src="web/preview/i18n.js">')
        html = html.replace('href="./" data-i18n="legacy"', 'href="#goals" data-i18n="home"')
        html = html.replace('data-i18n="preview">Design preview', 'data-i18n="publicTest">Public test')
        html = html.replace('Hytale Craft — Design preview', 'Hytale Craft — Public test')
        html = re.sub(r'<link rel="canonical"[^>]*>', '', html)
        html = html.replace('The current planner is available at the site root.', 'Enable JavaScript to use this tool.')
        if site_url:
            from html import escape
            origin = escape(site_url, quote=True)
            html = html.replace('</head>', '<link rel="canonical" href="'+origin+'/"><meta property="og:url" content="'+origin+'/"></head>')
        html = html.replace('</head>', '<meta property="og:title" content="Hytale Craft — Public test"><meta property="og:description" content="Pick a goal and plan your crafting resources. Unofficial Hytale player tool."><meta property="og:type" content="website"></head>')
        (out/'index.html').write_text(html)
        (out/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta name="robots" content="noindex"><title>404 — Hytale Craft</title><h1>404</h1><a href="/">Hytale Craft</a></html>')
        (out/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
        if site_url:
            from xml.sax.saxutils import escape
            (out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+escape(site_url+'/')+'</loc></url></urlset>')
        (out/'_redirects').write_text('/preview.html / 302\n')
        (out/'_headers').write_text("/*\n  X-Robots-Tag: noindex, nofollow\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: no-referrer\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'none'\n  Cache-Control: no-cache\n")
        hashes = {str(p.relative_to(out)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file()}
        (out/'build-manifest.json').write_text(json.dumps({'schema':1, 'testing':True, 'data_policy':policy, 'files':hashes}, indent=2)+'\n')
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(out, target)
    return target

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-policy', choices=('user-only','noncommercial-review'), default='user-only')
    parser.add_argument('--site-url', help='Future approved HTTPS origin; optional for review')
    args=parser.parse_args()
    (ROOT/'.private').mkdir(exist_ok=True)
    print(build(args.data_policy,args.site_url))
