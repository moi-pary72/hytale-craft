import hashlib
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pages',ROOT/'scripts/build_pages.py')
pages=importlib.util.module_from_spec(spec);spec.loader.exec_module(pages)
class PagesBuildTests(unittest.TestCase):
    def test_safe_output_and_new_entry(self):
        (ROOT/'.private').mkdir(exist_ok=True)
        out=pages.build()
        html=(out/'index.html').read_text()
        self.assertIn('id="goals"',html)
        self.assertIn('web/build-config.js',html)
        self.assertNotIn('data-i18n="legacy"',html)
        self.assertNotIn('github.io',html)
        self.assertFalse((out/'data').exists())
        self.assertFalse((out/'docs').exists())
        self.assertFalse((out/'tests').exists())
        self.assertFalse((out/'.git').exists())
        self.assertFalse((out/'locales/fr.json').exists())
        m=json.loads((out/'build-manifest.json').read_text())
        for name,sha in m['files'].items():
            self.assertEqual(hashlib.sha256((out/name).read_bytes()).hexdigest(),sha)
        self.assertIn('noindex',(out/'_headers').read_text())
        self.assertTrue((out/'404.html').exists())
    def test_explicit_noncommercial_data_and_origin(self):
        with self.assertRaises(ValueError):pages.build('noncommercial-review')
        out=pages.build('user-only','https://example.test')
        self.assertFalse((out/'data').exists())
        self.assertIn('https://example.test/',(out/'sitemap.xml').read_text())
        self.assertNotIn('previous',str(list(out.rglob('*'))))
        pages.build()
    def test_reject_unapproved_origin_shape(self):
        for origin in ('http://example.test','https://user:secret@example.test','https://example.test/path','https://example.test/?x=1'):
            with self.assertRaises(ValueError):pages.build(site_url=origin)

    def test_beta_assets_and_reproducible_output(self):
        out=pages.build();before=(out/'build-manifest.json').read_bytes();pages.build();self.assertEqual(before,(out/'build-manifest.json').read_bytes())
        self.assertIn('id="sheet"',(out/'index.html').read_text())
        for name in ('fight-poster','gather-poster','fight-atlas','gather-atlas'):self.assertTrue((out/'assets/art-pair'/f'{name}.webp').exists())
        for forbidden in ('assets/preview','web/preview/app.js','web/game-recipes.js','art-preview.html','preview.html','scripts','data','docs','tests','.private','.git'):
            self.assertFalse((out/forbidden).exists(),forbidden)

    def test_github_project_path_and_client_csp(self):
        out=pages.build(base_path='/hytale-craft/')
        self.assertIn('href="/hytale-craft/"',(out/'404.html').read_text())
        self.assertIn('http-equiv="Content-Security-Policy"',(out/'index.html').read_text())
        for path in ('//external.test/','/../','/x/?a=1'):
            with self.assertRaises(ValueError):pages.build(base_path=path)
        pages.build()

    def test_v2_artwork_integrity_and_no_source_masters(self):
        out=pages.build()
        names=('defend','build','survive','farm','explore','boss','skills','workshop','logo','frame','world','world-mobile','nav-home','nav-inventory','nav-plan','nav-more')
        self.assertEqual({p.stem for p in (out/'assets/ui-v2').glob('*.webp')},set(names))
        self.assertFalse((out/'assets/ui-v2/PROVENANCE.md').exists())
        self.assertFalse(any(out.rglob('*.png')))
        path=ROOT/'assets/ui-v2/build.webp';original=path.read_bytes()
        try:
            path.write_bytes(original+b'corruption')
            with self.assertRaisesRegex(ValueError,'UI artwork checksum mismatch'):pages.build()
        finally:path.write_bytes(original)
        pages.build()
