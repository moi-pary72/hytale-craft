import unittest,tempfile,json,copy
from pathlib import Path
from scripts.catalog_snapshot import stage
from scripts.import_catalog import ImportFailure
ROOT=Path(__file__).resolve().parents[1]
class SnapshotTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.data=json.loads((ROOT/'data/educational-canonical-v2.json').read_text());self.source=self.root/'input.json'
 def run_data(self,data):
  self.source.write_text(json.dumps(data));return stage(self.source,root=self.root)
 def test_immutable_versions_diff_and_last_good_survive_bad_import(self):
  a=self.run_data(self.data);self.assertTrue(a['written']);self.data['items'][0]['names']['en']='Changed original lesson';b=self.run_data(self.data);self.assertTrue(b['written']);self.assertNotEqual(a['snapshot'],b['snapshot']);self.assertTrue(b['changes']['items']['changed'])
  index=self.root/'.private/catalog-snapshots/index.json';old=index.read_bytes();bad=copy.deepcopy(self.data);bad['items'].append(bad['items'][0]);self.assertFalse(self.run_data(bad)['written']);self.assertEqual(index.read_bytes(),old);self.assertEqual(len(list(index.parent.glob('snapshots/*.json'))),2)
 def test_corrupted_prior_snapshot_blocks_update(self):
  a=self.run_data(self.data);(self.root/f'.private/catalog-snapshots/snapshots/{a["snapshot"]}.json').write_text('{}')
  with self.assertRaises(ImportFailure):self.run_data(self.data)
 def test_version_switch_needs_explicit_opt_in(self):
  self.run_data(self.data);self.data['snapshot']['game_version']='different imaginary version'
  for key in ['items','groups','stations','recipes']:
   for row in self.data[key]:row['game_version']='different imaginary version'
  self.assertFalse(self.run_data(self.data)['written'])
if __name__=='__main__':unittest.main()
