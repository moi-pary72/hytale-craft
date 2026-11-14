import hashlib,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('art',ROOT/'scripts/build_art_preview.py');art=importlib.util.module_from_spec(s);s.loader.exec_module(art)
class ArtPackagingTests(unittest.TestCase):
    def test_atlas_contract_and_hashes(self):
        d=json.loads((ROOT/'assets/art-pair/manifest.json').read_text());self.assertEqual(len(d['entries']),10);self.assertEqual(sum(v['status']=='sample' for v in d['entries'].values()),2);self.assertTrue(500<=d['duration_ms']<=1200)
        self.assertEqual(d['timeline'][-1],[900,None]);self.assertEqual(d['frame_size'],[480,320])
        for name,m in d['files'].items():
            raw=(ROOT/'assets/art-pair'/name).read_bytes();self.assertEqual(len(raw),m['bytes']);self.assertEqual(hashlib.sha256(raw).hexdigest(),m['sha256'])
        self.assertLess(sum(m['bytes'] for m in d['files'].values()),350000)
    def test_generated_page_is_current_isolated_and_noncommercial_data_free(self):
        self.assertEqual((ROOT/'art-preview.html').read_text(),art.create());self.assertIn('noindex',art.create());self.assertNotIn('rel="canonical"',art.create());self.assertIn('web/art-pair/config.js',art.create())
        self.assertIn("dataPolicy:'user-only'",(ROOT/'web/art-pair/config.js').read_text())
        source=(ROOT/'scripts/build_pages.py').read_text();self.assertNotIn('art-preview.html',source);self.assertNotIn('assets/art-pair',source)
    def test_offline_embeds_only_ui_and_art(self):
        html=art.create(True);self.assertNotIn('<script defer src=',html);self.assertNotIn('<link rel="stylesheet"',html);self.assertNotIn('Ingredient_Stick',html);self.assertNotIn('hysphere-2026-08-12.json',html);self.assertIn('data:image/webp;base64,',html);self.assertLess(len(html.encode()),600000)
