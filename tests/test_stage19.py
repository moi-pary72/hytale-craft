import unittest,tempfile,json,importlib.util
from pathlib import Path
from scripts.build_visual_registry import make_registry,ROOT
from scripts.build_stage19 import build
from scripts.build_real_data_lab import normalize
class Stage19Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):(ROOT/'.private').mkdir(exist_ok=True)
 def fixture(self):
  spec=importlib.util.spec_from_file_location('original_export',ROOT/'tests/helpers/research-export.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);manifest,items,recipes=m.export_fixture();return normalize(manifest,items,recipes,{}),items
 def test_registry_is_complete_without_invented_appearance_or_materials(self):
  bundle,items=self.fixture();r=make_registry(bundle,items);self.assertEqual(len(r['items']),4);self.assertEqual(len(set(r['priority100'])),4)
  for row in r['items']:self.assertIsNone(row['material']['confirmed']);self.assertEqual(row['appearance']['confidence'],'unknown')
 def test_registry_rejects_mixed_item_revisions_and_missing_records(self):
  bundle,items=self.fixture();items['extractedAt']='different'
  with self.assertRaises(ValueError):make_registry(bundle,items)
 def test_public_mode_refuses_research_inputs_before_copying(self):
  with tempfile.TemporaryDirectory(dir=ROOT/'.private')as tmp:
   out=Path(tmp)/'out'
   with self.assertRaisesRegex(ValueError,'research inputs'):build('PUBLIC_RELEASE',out,input_dir=ROOT/'.private')
   self.assertFalse(out.exists())
 def test_private_mode_needs_acknowledgement_and_outputs_cannot_be_public(self):
  with tempfile.TemporaryDirectory(dir=ROOT/'.private')as tmp:
   with self.assertRaisesRegex(ValueError,'authorized inputs'):build('PRIVATE_REAL_DATA',Path(tmp)/'out')
  with self.assertRaises(ValueError):build('PUBLIC_RELEASE',ROOT/'public-stage19')
if __name__=='__main__':unittest.main()
