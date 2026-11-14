import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from scripts.import_game_assets import extract, material
from scripts.sync_catalog import normalize, save

class ImportTests(unittest.TestCase):
    def archive(self, rows):
        temp=tempfile.NamedTemporaryFile(suffix='.zip',delete=False)
        self.addCleanup(Path(temp.name).unlink)
        with zipfile.ZipFile(temp,'w') as z:
            for p,v in rows.items():z.writestr('Server/Item/'+p,json.dumps(v))
        return temp.name
    def test_explicit_and_implicit(self):
        d=extract(self.archive({'Items/TestRaw.json':{},'Items/TestMade.json':{'Recipe':{'Input':[{'ItemId':'TestRaw','Quantity':3}],'OutputQuantity':2,'BenchRequirement':[{'Id':'TestBench'}]}}}))
        self.assertEqual(d['recipe_count'],1)
        self.assertEqual(d['recipes'][0]['outputs'][0]['quantity'],2)
        self.assertTrue(d['recipes'][0]['calculation_supported'])
        self.assertEqual(d['recipes'][0]['bench_requirements'],[{'Id':'TestBench'}])
    def test_reject_inherited_and_invalid_output(self):
        d=extract(self.archive({'Items/Test.json':{'Parent':'Missing','Recipe':{}},'Items/TestBad.json':{'Recipe':{'Input':[{'ItemId':'X'}],'Output':[{'ItemId':'Y','Quantity':0}]}}}))
        self.assertEqual(d['recipe_count'],0)
        self.assertEqual(d['rejected_count'],2)
    def test_material(self):
        for x in ({'ItemId':'X','Quantity':True},{'ItemId':'X','ItemTag':'T'},{'ItemId':'X','Quantity':-1}):self.assertIsNone(material(x))
    def test_catalog_does_not_invent_recipes(self):
        d=normalize(['Test_Item'],['Test_Recipe'],{'generated_at':'2026-07-06'})
        self.assertEqual(d['recipes'],[])
        self.assertIsNone(d['items'][0]['names']['ru'])
        with self.assertRaises(ValueError):normalize(['X','X'],['R'],{'generated_at':'date'})
    def test_preserve_on_shrink(self):
        with tempfile.TemporaryDirectory() as p:
            dest=Path(p)/'catalog.json'
            save({'items':list(range(10))},dest)
            before=dest.read_bytes()
            with self.assertRaises(ValueError):save({'items':[1]},dest)
            self.assertEqual(before,dest.read_bytes())

if __name__=='__main__':unittest.main()
