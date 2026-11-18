"""Synthetic-only packaging checks; never introduce real private exports into CI."""
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from scripts.build_real_data_lab import build, ROOT
from scripts.package_private_lab import package, BUNDLE_FOLDER

spec = importlib.util.spec_from_file_location('fixture',ROOT/'tests/helpers/research-export.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)

class PrivatePackageTests(unittest.TestCase):
    def test_private_package_only_contains_build_and_local_server(self):
        (ROOT/'.private').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'.private') as td:
            home=Path(td)
            inp=home/'input'
            inp.mkdir()
            for name,obj in zip(('manifest','items','recipes'),fixture.export_fixture()):
                (inp/(name+'.json')).write_text(json.dumps(obj))
            lab=home/'build'
            build(inp,lab,True)
            output=home/'owner-local.zip'
            report=package(lab,output)
            self.assertTrue(output.is_file())
            self.assertEqual(report['metrics']['items'],4)
            with zipfile.ZipFile(output) as archive:
                self.assertIsNone(archive.testzip())
                names=set(archive.namelist())
                self.assertIn(BUNDLE_FOLDER+'/research-data.json',names)
                self.assertIn('start_local.sh',names)
                self.assertIn('scripts/serve_real_data_lab.py',names)
                self.assertNotIn('manifest.json',names)
                self.assertFalse(any(name.startswith('.git/') or '/input/' in name for name in names))
                policy=json.loads(archive.read('PRIVATE_PACKAGE_MANIFEST.json'))
                self.assertTrue(policy['no_public_distribution'])
            with self.assertRaises(ValueError):package(lab,output)
            with self.assertRaises(ValueError):package(lab,ROOT/'public-private.zip')
            (lab/'research-data.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'checksum mismatch'):
                package(lab,home/'corrupt.zip')

if __name__=='__main__': unittest.main()
