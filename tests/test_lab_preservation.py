import unittest,tempfile,json,hashlib
from pathlib import Path
from scripts.verify_real_data_lab import verify,ROOT
class PreservationTests(unittest.TestCase):
 def test_pinned_manifest_validates_bytes_and_detects_corruption_without_network(self):
  with tempfile.TemporaryDirectory(dir=ROOT/'.private') as tmp:
   p=Path(tmp);files={}
   for name in ['manifest.json','items.json','recipes.json']:
    (p/name).write_bytes(b'{}');files[name]={'sha256':hashlib.sha256(b'{}').hexdigest()}
   manifest=p/'checks.json';manifest.write_text(json.dumps({'files':files,'source_revision':'synthetic','normalization_date':'2026-11-16'}));self.assertTrue(verify(p,manifest)['raw_integrity']);(p/'items.json').write_bytes(b'bad')
   with self.assertRaisesRegex(ValueError,'checksum'):verify(p,manifest)
 def test_public_paths_rejected(self):
  with self.assertRaises(ValueError):verify(ROOT/'dist')
if __name__=='__main__':unittest.main()
