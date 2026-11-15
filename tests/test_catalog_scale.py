"""Large ORIGINAL generated catalogue; no network, game records or public writes."""
import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from scripts import import_catalog_v2 as importer

class CatalogScaleTests(unittest.TestCase):
    def test_large_import_hashes_and_invalid_replacement_preserves_candidate(self):
        data=json.loads((Path(__file__).parent/'fixtures/catalog-v2-synthetic.json').read_text())
        item=copy.deepcopy(data['items'][0]);recipe=copy.deepcopy(data['recipes'][0]);data['items']=[dict(item,id='load:raw')];data['groups']=[];data['recipes']=[]
        for i in range(5000):
            key=f'load:item-{i}';data['items'].append(dict(item,id=key,source_record=f'generated/{i}'))
            row=copy.deepcopy(recipe);row.update(id=f'load:recipe-{i}',source_record=f'generated/recipe/{i}',inputs=[{'quantity':2,'options':[{'kind':'item','id':'load:raw'}]}],outputs=[{'item_id':key,'quantity':1}],primary_output=key);data['recipes'].append(row)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'original-load.json';source.write_text(json.dumps(data));digest=hashlib.sha256(source.read_bytes()).hexdigest()
            report=importer.run(source,root=root,expected_sha256=digest);self.assertTrue(report['written'],report['errors']);self.assertEqual(report['counts']['recipes'],5000)
            path=root/'.private/catalog-v2-candidate.json';before=path.read_bytes();candidate=json.loads(before);self.assertEqual(len(candidate['record_sha256']['recipes']),5000);self.assertEqual(candidate['publication']['status'],'blocked');self.assertEqual(candidate['import_provenance']['input_sha256'],digest)
            data['recipes'][-1]['outputs'][0]['item_id']='missing';source.write_text(json.dumps(data));invalid=importer.run(source,root=root);self.assertFalse(invalid['written']);self.assertTrue(invalid['errors']);self.assertEqual(path.read_bytes(),before)

if __name__=='__main__':unittest.main()
