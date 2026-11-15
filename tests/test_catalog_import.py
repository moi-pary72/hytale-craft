"""Original synthetic fixtures only: no game recipe or third-party snapshot."""
import copy,json,tempfile,unittest
from pathlib import Path
from scripts.import_catalog import validate,strict_json,run,ImportFailure,STATES
FIXTURE=Path(__file__).parent/'fixtures/catalog-synthetic.json'
class CatalogImportTests(unittest.TestCase):
    def data(self):return json.loads(FIXTURE.read_text())
    def invalid(self,mutate,word):
        d=self.data();mutate(d);errors,_=validate(d);self.assertTrue(any(word in x['message'] for x in errors),errors)
    def test_original_fixture_is_structurally_valid(self):self.assertEqual(validate(self.data()),([],[]))
    def test_quantities_are_strict_positive_integers(self):
        for q in (0,-1,1.5,True,'2',1000000):
            self.invalid(lambda d:d['recipes'][0]['inputs'][0].update(quantity=q),'positive')
    def test_broken_references_and_stations(self):
        self.invalid(lambda d:d['recipes'][0]['inputs'][0].update(item_id='Missing'),'Unknown item')
        self.invalid(lambda d:d['recipes'][0].update(stations=['Missing']),'Unknown station')
        self.invalid(lambda d:d['items'][0].update(source_id='Missing'),'Unknown source')
    def test_duplicates(self):
        for key in ('items','recipes','stations','sources'):
            self.invalid(lambda d:d[key].append(copy.deepcopy(d[key][0])),'Duplicate identifier')
        self.invalid(lambda d:d['recipes'][0]['inputs'].append(copy.deepcopy(d['recipes'][0]['inputs'][0])),'Duplicate material')
        with self.assertRaises(ImportFailure):strict_json('{"x":1,"x":2}')
    def test_cycles(self):
        self.invalid(lambda d:d['recipes'][0]['inputs'][0].update(item_id='Fixture_Part'),'Recipe cycle')
        self.invalid(lambda d:d['recipes'][0]['inputs'][0].update(item_id='Fixture_Product'),'Recipe cycle')
    def test_schema_version_timezone_and_empty_inputs(self):
        self.invalid(lambda d:d.update(schema_version=2),'Unsupported schema')
        self.invalid(lambda d:d['snapshot'].update(updated_at='2026-11-15'),'timezone')
        self.invalid(lambda d:d.update(recipes=[]),'nonempty')
        self.invalid(lambda d:d['recipes'][0].update(inputs=[]),'Nonempty material')
        self.invalid(lambda d:d['items'][0].update(game_version='different'),'Mixed game')
    def test_names_unknown_rights_and_status(self):
        self.invalid(lambda d:d['items'][0].update(names={'en':42}),'language map')
        self.invalid(lambda d:d['items'][0].update(status='official'),'verification state')
        d=self.data();d['sources'][0]['license']['commercial_use']='unknown';errors,warnings=validate(d);self.assertFalse(errors);self.assertTrue(warnings)
    def test_declared_verified_does_not_authorize_publication(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'input.json';d=self.data();d['items'][0]['status']='verified';source.write_text(json.dumps(d));r=run(source,root=root)
            self.assertTrue(r['written']);candidate=json.loads((root/'.private/catalog-candidate.json').read_text());self.assertEqual(candidate['publication']['status'],'blocked');self.assertTrue(candidate['publication']['approval_required'])
    def test_atomic_failure_preserves_previous_and_version_change_backed_up(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'input.json';source.write_bytes(FIXTURE.read_bytes());self.assertTrue(run(source,root=root)['written']);out=root/'.private/catalog-candidate.json';before=out.read_bytes()
            for raw in (b'BROKEN',b'{"schema_version":1}',b'{"x":NaN}'):
                source.write_bytes(raw);r=run(source,root=root);self.assertFalse(r['written']);self.assertTrue(r['errors']);self.assertEqual(before,out.read_bytes())
            d=self.data();d['snapshot']['game_version']='synthetic-test-v2';source.write_text(json.dumps(d));self.assertFalse(run(source,root=root)['written']);self.assertEqual(before,out.read_bytes());self.assertTrue(run(source,root=root,allow_version_change=True)['written']);backups=list((root/'.private').glob('*.previous'));self.assertEqual(len(backups),1);self.assertEqual(before,backups[0].read_bytes())
    def test_reproducible_no_public_writes_or_input_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'input.json';source.write_bytes(FIXTURE.read_bytes());run(source,root=root);out=root/'.private/catalog-candidate.json';before=out.read_bytes();run(source,root=root);self.assertEqual(before,out.read_bytes())
            with self.assertRaises(ImportFailure):run(source,output='data/catalog.json',root=root)
            with self.assertRaises(ImportFailure):run(source,output=source,root=root)
            with self.assertRaises(ImportFailure):run(source,report='.private/catalog-candidate.json',root=root)
    def test_oversize_and_symlink_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'input.json';source.write_bytes(b' '*10000001);self.assertFalse(run(source,root=root)['written']);source.write_bytes(FIXTURE.read_bytes());(root/'.private/link.json').symlink_to(source)
            with self.assertRaises(ImportFailure):run(source,output='.private/link.json',root=root)
    def test_all_states_and_multiple_outputs_are_preserved(self):
        for status in STATES:
            d=self.data();d['items'][0]['status']=status;self.assertFalse(validate(d)[0])
        d=self.data();extra=copy.deepcopy(d['items'][0]);extra['id']='Fixture_Byproduct';d['items'].append(extra);d['recipes'][1]['outputs'].append({'item_id':'Fixture_Byproduct','quantity':1});self.assertFalse(validate(d)[0]);self.assertTrue(any('Multiple outputs' in w['message'] for w in validate(d)[1]))

    def test_expected_hash_mismatch_preserves_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'input.json';source.write_bytes(FIXTURE.read_bytes());run(source,root=root);out=root/'.private/catalog-candidate.json';before=out.read_bytes()
            result=run(source,root=root,expected_sha256='0'*64);self.assertFalse(result['written']);self.assertIn('SHA-256',result['errors'][0]['message']);self.assertEqual(out.read_bytes(),before)
