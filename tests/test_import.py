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


class AdvancedImportTests(unittest.TestCase):
    archive=ImportTests.archive
    def test_parent_override_and_cycle(self):
        d=extract(self.archive({'Items/Raw.json':{},'Items/Base.json':{'Recipe':{'Input':[{'ItemId':'Raw','Quantity':2}],'OutputQuantity':1}},'Items/Child.json':{'Parent':'Base','Recipe':{'OutputQuantity':3}}}))
        row=next(r for r in d['recipes'] if r['outputs'][0]['id']=='Child')
        self.assertEqual(row['inputs'][0]['quantity'],2)
        self.assertEqual(row['outputs'][0]['quantity'],3)
        c=extract(self.archive({'Items/A.json':{'Parent':'B'},'Items/B.json':{'Parent':'A'}}))
        self.assertEqual(c['rejected_count'],2)
    def test_material_groups_preserved_without_guessing(self):
        d=extract(self.archive({'Items/A.json':{'Recipe':{'Input':[{'ResourceTypeId':'AnyWood','Quantity':2}]}}}))
        self.assertEqual(d['recipes'][0]['inputs'][0]['kind'],'ResourceTypeId')
        self.assertFalse(d['recipes'][0]['calculation_supported'])
    def test_multiple_and_primary_outputs_preserved(self):
        d=extract(self.archive({'Items/A.json':{},'Items/B.json':{},'Recipes/Test.json':{'Input':[{'ItemId':'A'}],'Output':[{'ItemId':'B','Quantity':2},{'ItemId':'A'}],'PrimaryOutput':{'ItemId':'B','Quantity':2}}}))
        self.assertEqual(len(d['recipes'][0]['outputs']),2)
        self.assertEqual(d['recipes'][0]['primary_output']['id'],'B')
        self.assertFalse(d['recipes'][0]['calculation_supported'])


class ImportCliTests(unittest.TestCase):
    archive=ImportTests.archive
    def test_checksum_failure_preserves_candidate(self):
        import subprocess,sys
        source=self.archive({'Items/Raw.json':{},'Items/Made.json':{'Recipe':{'Input':[{'ItemId':'Raw'}]}}})
        with tempfile.TemporaryDirectory() as p:
            output=Path(p)/'candidate.json';output.write_text('previous')
            proc=subprocess.run([sys.executable,'scripts/import_game_assets.py',source,'--game-version','fixture','--expected-sha256','0'*64,'--output',str(output),'--report',str(Path(p)/'report.json')],capture_output=True)
            self.assertNotEqual(proc.returncode,0);self.assertEqual(output.read_text(),'previous')
    def test_invalid_assets_preserve_candidate_and_report_error(self):
        import subprocess,sys
        source=self.archive({'Items/Bad.json':{'Parent':'Missing'}})
        with tempfile.TemporaryDirectory() as p:
            output=Path(p)/'candidate.json';output.write_text('previous');report=Path(p)/'report.json'
            proc=subprocess.run([sys.executable,'scripts/import_game_assets.py',source,'--game-version','fixture','--output',str(output),'--report',str(report)],capture_output=True)
            self.assertNotEqual(proc.returncode,0);self.assertEqual(output.read_text(),'previous');self.assertEqual(json.loads(report.read_text())['rejected_count'],1)

if __name__=='__main__':unittest.main()
