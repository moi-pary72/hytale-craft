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
        out=pages.build('noncommercial-review','https://example.test')
        self.assertTrue((out/'data/recipes/manifest.json').exists())
        self.assertIn('https://example.test/',(out/'sitemap.xml').read_text())
        self.assertNotIn('previous',str(list(out.rglob('*'))))
        pages.build()
    def test_reject_unapproved_origin_shape(self):
        for origin in ('http://example.test','https://user:secret@example.test','https://example.test/path','https://example.test/?x=1'):
            with self.assertRaises(ValueError):pages.build(site_url=origin)
