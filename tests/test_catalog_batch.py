"""Own synthetic fixtures; no credentials or foreign records."""
import json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import prepare_catalog_batch as m,fetch_hytl_batch as f
class Batch(unittest.TestCase):
 def test_candidate_is_private_and_never_auto_approved(self):
  (m.base.ROOT/'.private').mkdir(exist_ok=True)
  with tempfile.TemporaryDirectory(dir=m.base.ROOT/'.private') as d:
   root=Path(d);source=root/'source.json';source.write_text((m.base.ROOT/'tests/fixtures/catalog-v2-synthetic.json').read_text());out=root/'result';r=m.prepare(source,out);self.assertEqual(sum(r['groups'].values()),r['items']);self.assertEqual(r['groups']['A'],0);self.assertEqual(json.loads((out/'records.json').read_text())['publication'],'blocked')
   with self.assertRaises(ValueError):m.prepare(source,out)
   v=json.loads(source.read_text());v['items'].append(v['items'][0]);source.write_text(json.dumps(v))
   with self.assertRaises(ValueError):m.prepare(source,root/'invalid')
   self.assertFalse((root/'invalid').exists())
 def test_no_key_no_request_and_no_redirect_credentials(self):
  with patch.dict(os.environ,{},clear=True),patch('urllib.request.build_opener') as request:
   with self.assertRaises(ValueError):f.fetch('items',0,m.base.ROOT/'.private/never-hytl.json')
   request.assert_not_called()
  with self.assertRaises(ValueError):f.NoRedirect().redirect_request(None,None,None,None,None,None)
if __name__=='__main__':unittest.main()
