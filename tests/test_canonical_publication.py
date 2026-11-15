"""Rights approval is trusted reviewed configuration, not source-provided flags."""
import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gate',ROOT/'scripts/canonical_publication.py');gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
class CanonicalPublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);(self.root/'data').mkdir()
        for name in ['educational-canonical-v2.json','educational-publication-approval.json']:(self.root/'data'/name).write_bytes((ROOT/'data'/name).read_bytes())
    def test_only_reviewed_original_learning_data(self):
        data,approval,raw=gate.approved_learning(self.root);self.assertEqual(len(data['recipes']),4);self.assertFalse(approval['game_data']);self.assertEqual(data['snapshot']['channel'],'test')
    def test_declared_source_permission_does_not_override_checksum(self):
        p=self.root/'data/educational-canonical-v2.json';d=json.loads(p.read_text());d['items'][0]['names']['en']='Changed source';p.write_text(json.dumps(d))
        with self.assertRaises(ValueError):gate.approved_learning(self.root)
    def test_missing_or_non_original_approval_blocked(self):
        p=self.root/'data/educational-publication-approval.json';a=json.loads(p.read_text());a['game_data']=True;p.write_text(json.dumps(a))
        with self.assertRaises(ValueError):gate.approved_learning(self.root)
        p.unlink()
        with self.assertRaises(OSError):gate.approved_learning(self.root)
    def test_publication_input_symlink_blocked(self):
        p=self.root/'data/educational-canonical-v2.json';p.unlink();p.symlink_to(ROOT/'data/educational-canonical-v2.json')
        with self.assertRaises(ValueError):gate.approved_learning(self.root)
if __name__=='__main__':unittest.main()
