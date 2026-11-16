#!/usr/bin/env python3
"""Prepare a static, noindex review build. Never deploys or downloads anything."""
import argparse
import hashlib
import json
import os
import subprocess
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ('en', 'ru', 'es', 'pt-BR')

def build(policy='user-only', site_url=None, base_path='/', guide=False):
    if base_path != '/' and not re.fullmatch(r'/[a-zA-Z0-9_-]+/',base_path):
        raise ValueError('Invalid publication base path')
    if policy != 'user-only':
        raise ValueError('Public beta supports user-only; use export_preview.py for restricted owner review')
    if site_url:
        u = urlsplit(site_url)
        if u.scheme != 'https' or not u.hostname or u.username or u.password or u.query or u.fragment or u.path not in ('', '/'):
            raise ValueError('SITE_URL must be an HTTPS origin without credentials, query or path')
        site_url = site_url.rstrip('/')
    revision = os.environ.get('CF_PAGES_COMMIT_SHA') or os.environ.get('GITHUB_SHA')
    if not revision:
        revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('Invalid build revision')
    (ROOT/'.private').mkdir(exist_ok=True)
    target = ROOT / 'dist'
    if target.is_symlink():
        raise ValueError('dist must not be a symlink')
    with tempfile.TemporaryDirectory(prefix='pages-', dir=ROOT / '.private') as tmp:
        out = Path(tmp)
        paths = ['web/craftable.js', 'web/beta/deep.js', 'web/beta/deep.css', 'web/item-visuals.js','web/item-visuals.css','assets/item-system/categories.webp','assets/item-system/extended.webp','web/planner.js', 'web/preview/i18n.js', 'web/beta/app.js', 'web/beta/style.css', 'web/beta/examples.js', 'web/beta/workspace.js', 'web/planner-v2.js', 'web/canonical-adapter.js']
        paths += ['locales/' + lang + '.json' for lang in LANGUAGES]
        paths += ['locales/beta/' + lang + '.json' for lang in LANGUAGES]
        paths += ['assets/art-pair/' + name + '.webp' for name in ('fight-poster','gather-poster','fight-atlas','gather-atlas')]
        art_manifest=json.loads((ROOT/'assets/art-pair/manifest.json').read_text())
        if set(art_manifest['files']) != {'fight-poster.webp','gather-poster.webp','fight-atlas.webp','gather-atlas.webp'}:
            raise ValueError('Incomplete art manifest')
        for name,meta in art_manifest['files'].items():
            if Path(name).name!=name or name not in ('fight-poster.webp','gather-poster.webp','fight-atlas.webp','gather-atlas.webp'):
                raise ValueError('Unsafe art resource')
            raw=(ROOT/'assets/art-pair'/name).read_bytes()
            if hashlib.sha256(raw).hexdigest()!=meta['sha256']:
                raise ValueError('Art checksum mismatch')
        ui_names = ('defend', 'build', 'survive', 'farm', 'explore', 'boss', 'skills', 'workshop', 'world', 'world-mobile', 'logo', 'frame', 'nav-home', 'nav-inventory', 'nav-plan', 'nav-more')
        ui_manifest=json.loads((ROOT/'assets/ui-v2/manifest.json').read_text())
        if set(ui_manifest['files']) != {name+'.webp' for name in ui_names}:
            raise ValueError('Incomplete UI artwork manifest')
        for name,meta in ui_manifest['files'].items():
            src=ROOT/'assets/ui-v2'/name
            if src.is_symlink() or hashlib.sha256(src.read_bytes()).hexdigest()!=meta['sha256']:
                raise ValueError('UI artwork checksum mismatch: '+name)
            paths.append('assets/ui-v2/'+name)
        item_manifest=json.loads((ROOT/'assets/learning-items/manifest.json').read_text())
        if set(item_manifest)!={k+'.webp' for k in ('blade','strip','stone','fibre','pick','panel','wood')}:raise ValueError('Unexpected learning art')
        for name,sha in item_manifest.items():
            src=ROOT/'assets/learning-items'/name
            if src.is_symlink() or hashlib.sha256(src.read_bytes()).hexdigest()!=sha:raise ValueError('Learning art integrity')
            paths.append('assets/learning-items/'+name)
        import importlib.util
        visual_spec=importlib.util.spec_from_file_location('item_visuals_integrity',Path(__file__).with_name('item_visuals_integrity.py'))
        visual_module=importlib.util.module_from_spec(visual_spec);visual_spec.loader.exec_module(visual_module)
        verify_visuals=visual_module.verify
        verify_visuals(ROOT)
        # Legacy SVG scenes are excluded from beta output.
        for name in paths:
            src = ROOT/name
            if src.is_symlink():
                raise ValueError('Symlink input forbidden')
            dest = out/name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)
        import importlib.util
        spec=importlib.util.spec_from_file_location('canonical_publication',ROOT/'scripts/canonical_publication.py');gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
        learning,approval,raw=gate.approved_learning(ROOT)
        (out/'web/beta/advanced-data.json').write_bytes(raw)
        config = {'canonicalApproval':approval, 'guideUX':guide, 'testing': True, 'dataPolicy': 'user-only', 'requestTimeoutMs': 12000}
        (out/'web/build-config.js').write_text('window.CRAFT_BUILD='+json.dumps(config)+';\n')
        html = (ROOT/'beta.html').read_text()
        html = html.replace('<script defer src="web/preview/i18n.js">', '<script defer src="web/build-config.js"></script><script defer src="web/preview/i18n.js">')
        html = re.sub(r'<link rel="canonical"[^>]*>', '', html)
        if site_url:
            from html import escape
            origin = escape(site_url, quote=True)
            html = html.replace('</head>', '<link rel="canonical" href="'+origin+'/"><meta property="og:url" content="'+origin+'/"></head>')
        html = html.replace('</head>', '<meta property="og:title" content="Hytale Craft — Beta"><meta property="og:description" content="Pick a goal and plan your crafting resources. Unofficial Hytale player tool."><meta property="og:type" content="website"></head>')
        # GitHub Pages cannot serve custom _headers; enforce the compatible policy in HTML too.
        html=html.replace('</head>',"<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'\"></head>")
        (out/'index.html').write_text(html)
        (out/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta name="robots" content="noindex"><title>404 — Hytale Craft</title><h1>404</h1><a href="'+base_path+'">Hytale Craft</a></html>')
        (out/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
        if site_url:
            from xml.sax.saxutils import escape
            (out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+escape(site_url+'/')+'</loc></url></urlset>')
        (out/'_redirects').write_text('/preview.html / 302\n/art-preview.html / 302\n/beta.html / 302\n')
        (out/'_headers').write_text("/*\n  X-Robots-Tag: noindex, nofollow\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: no-referrer\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'none'\n  Cache-Control: no-cache\n")
        hashes = {str(p.relative_to(out)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file()}
        (out/'build-manifest.json').write_text(json.dumps({'schema':1, 'testing':True, 'data_policy':policy, 'revision':revision, 'real_game_recipes':0, 'files':hashes}, indent=2)+'\n')
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(out, target)
    return target

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-policy', choices=('user-only',), default='user-only')
    parser.add_argument('--site-url', help='Future approved HTTPS origin; optional for review')
    parser.add_argument('--base-path', default='/', help='GitHub project path for 404 home link; Cloudflare uses /')
    args=parser.parse_args()
    (ROOT/'.private').mkdir(exist_ok=True)
    print(build(args.data_policy,args.site_url,args.base_path,guide=True))
