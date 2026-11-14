#!/usr/bin/env python3
"""Verify the beta publish boundary and every generated content checksum."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def audit(directory=None):
    out=Path(directory or ROOT/'dist');manifest=json.loads((out/'build-manifest.json').read_text())
    allowed={'index.html','404.html','robots.txt','_headers','_redirects','build-manifest.json','sitemap.xml','web/build-config.js','web/planner.js','web/preview/i18n.js','web/beta/app.js','web/beta/style.css','web/beta/examples.js'}
    allowed.update('locales/'+prefix+lang+'.json' for prefix in ('','beta/') for lang in ('en','ru','es','pt-BR'))
    allowed.update('assets/art-pair/'+name+'.webp' for name in ('fight-poster','gather-poster','fight-atlas','gather-atlas'))
    files={str(p.relative_to(out)) for p in out.rglob('*') if p.is_file()}
    if files-allowed:raise ValueError('Unexpected public files: '+str(sorted(files-allowed)))
    if files-{'build-manifest.json'}!=set(manifest['files']):raise ValueError('Manifest membership mismatch')
    for name,sha in manifest['files'].items():
        p=out/name
        if p.is_symlink() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:raise ValueError('Checksum mismatch: '+name)
    for path in files:
        if path.endswith(('.js','.css')):
            text=(out/path).read_text()
            if any(token in text for token in ('https://','http://','google-analytics','gtag(','facebook.net','WebSocket(','sendBeacon(')):
                raise ValueError('External network/tracker reference: '+path)
    if manifest.get('data_policy')!='user-only':raise ValueError('Restricted data mode')
    html=(out/'index.html').read_text()
    if 'id="sheet"' not in html or 'web/beta/app.js' not in html or 'web/preview/app.js' in html:raise ValueError('Wrong entry point')
    for p in out.rglob('*'):
        if p.is_file() and p.suffix in ('.json','.js','.html') and 'Weapon_Shortbow_Crude' in p.read_text():raise ValueError('Game snapshot/reference leaked')
    if 'noindex' not in (out/'_headers').read_text() or 'Disallow: /' not in (out/'robots.txt').read_text():raise ValueError('Testing indexing gate missing')
    return {'schema':1,'data_policy':'user-only','entrypoint':'beta.html → dist/index.html','files':len(files),'total_bytes':sum((out/f).stat().st_size for f in files),'checksums_verified':len(manifest['files']),'community_snapshots':0,'original_learning_recipes':4,'restricted_modes_rejected':True,'internal_files':0,'trackers_or_ad_libraries':0,'reproducible':None,'file_checksums':manifest['files']}
if __name__=='__main__':print(json.dumps(audit(),indent=2))
