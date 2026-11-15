"""Original synthetic canonical-v2 fixtures; no real Hytale records or network."""
import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from scripts import import_catalog_v2 as m
ROOT=Path(__file__).resolve().parents[1]
class CatalogV2Tests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'tests/fixtures/catalog-v2-synthetic.json').read_text())
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name);self.source=self.root/'original.json';self.write()
    def write(self):self.source.write_text(json.dumps(self.data))
    def run_import(self,**kw):return m.run(self.source,root=self.root,**kw)
    def test_original_fixture_preserves_complex_features_and_never_publishes(self):
        r=self.run_import();self.assertTrue(r['written'],r);v=json.loads((self.root/'.private/catalog-v2-candidate.json').read_text());self.assertEqual(v['publication']['status'],'blocked');self.assertTrue(v['publication']['approval_required']);self.assertEqual(v['groups'],self.data['groups']);self.assertEqual(v['recipes'],self.data['recipes']);self.assertFalse(v['calculation_capabilities']['sample:make-device']['legacy_arithmetic_shape']);self.assertEqual(len(v['record_sha256']['recipes']),4)
    def test_alternative_recipes_not_deduplicated_by_output(self):
        e,w,c=m.validate(self.data);self.assertFalse(e);self.assertIn('sample:make-part',c);self.assertIn('sample:alternate-part',c);self.assertIn('alternative_input',c['sample:alternate-part']['unsupported_features'])
    def test_zero_boolean_fraction_and_huge_quantities_rejected(self):
        for value in [0,-1,True,1.5,1000000,'2']:
            v=copy.deepcopy(self.data);v['recipes'][0]['inputs'][0]['quantity']=value;self.assertTrue(m.validate(v)[0],value)
        self.data['groups'][0]['members'][0]['units']=0;self.assertTrue(m.validate(self.data)[0])
    def test_unknown_material_group_output_station_and_source_references(self):
        for field in ['input','group','output','station','source']:
            v=copy.deepcopy(self.data)
            if field=='input':v['recipes'][0]['inputs'][0]['options'][0]['id']='absent'
            if field=='group':v['recipes'][1]['inputs'][1]['options'][0]['id']='absent'
            if field=='output':v['recipes'][0]['outputs'][0]['item_id']='absent'
            if field=='station':v['recipes'][0]['station_requirements']['entries'][0]['station_id']='absent'
            if field=='source':v['groups'][0]['source_id']='absent'
            self.assertTrue(m.validate(v)[0],field)
    def test_duplicate_ids_options_members_and_outputs_rejected(self):
        for where in ['id','option','member','output']:
            v=copy.deepcopy(self.data)
            if where=='id':v['recipes'].append(copy.deepcopy(v['recipes'][0]))
            if where=='option':v['recipes'][0]['inputs'][0]['options']*=2
            if where=='member':v['groups'][0]['members']*=2
            if where=='output':v['recipes'][0]['outputs']*=2
            self.assertTrue(m.validate(v)[0],where)
    def test_primary_output_is_existing_output_not_extra_product(self):
        self.data['recipes'][1]['primary_output']='sample:raw-a';self.assertTrue(m.validate(self.data)[0]);self.data['recipes'][1]['primary_output']=None;self.assertFalse(m.validate(self.data)[0])
    def test_incomplete_groups_are_preserved_with_warning(self):
        g=self.data['groups'][0];g.update(members=[],selection='unknown',membership_complete=False);e,w,c=m.validate(self.data);self.assertFalse(e);self.assertTrue(any('Group membership' in x['message'] for x in w));g['membership_complete']=True;self.assertTrue(m.validate(self.data)[0])
    def test_levels_station_types_and_unlocks_validated(self):
        for field,value in [('min_level',-1),('min_level',True),('type','Invented')]:
            v=copy.deepcopy(self.data);v['recipes'][0]['station_requirements']['entries'][0][field]=value;self.assertTrue(m.validate(v)[0])
        self.data['recipes'][0]['requirements']['knowledge_required']='false';self.assertTrue(m.validate(self.data)[0])
    def test_salvage_reversal_cycle_separate_from_crafting(self):
        e,w,c=m.validate(self.data);self.assertFalse(e);self.assertTrue(any('all_transformations cycle' in x['message'] for x in w));self.assertFalse(any('craft_processing cycle' in x['message'] for x in w));self.assertTrue(c['sample:make-part']['legacy_arithmetic_shape']);self.assertFalse(c['sample:recycle-device']['legacy_arithmetic_shape'])
    def test_craft_cycles_conservatively_block_arithmetic_shape(self):
        self.data['recipes'][0]['inputs'][0]['options'][0]['id']='sample:part';e,w,c=m.validate(self.data);self.assertFalse(e);self.assertTrue(any('craft_processing cycle' in x['message'] for x in w));self.assertTrue(all(not x['legacy_arithmetic_shape'] for x in c.values()))
    def test_rights_declarations_cannot_enable_publication(self):
        self.data['sources'][0]['license'].update(commercial_use='prohibited',redistribution='unknown');self.write();r=self.run_import();self.assertTrue(r['written']);self.assertEqual(r['publication'],'blocked-pending-owner-and-rights-review');self.assertTrue(r['warnings'])
    def test_mixed_version_and_malformed_snapshot_are_errors(self):
        self.data['recipes'][0]['game_version']='different';self.assertTrue(m.validate(self.data)[0]);self.data['snapshot']=[];self.assertTrue(m.validate(self.data)[0]);self.assertTrue(m.validate({'schema_version':2})[0])
    def test_checksum_bad_json_and_duplicate_keys_preserve_previous(self):
        self.assertTrue(self.run_import()['written']);out=self.root/'.private/catalog-v2-candidate.json';before=out.read_bytes()
        self.assertFalse(self.run_import(expected_sha256='0'*64)['written']);self.assertEqual(out.read_bytes(),before)
        for raw in ['BROKEN','{"schema_version":2,"schema_version":2}']:
            self.source.write_text(raw);self.assertFalse(self.run_import()['written']);self.assertEqual(out.read_bytes(),before)
    def test_determinism_version_diff_and_backup(self):
        first=self.run_import();second=self.run_import();self.assertEqual(first['candidate_sha256'],second['candidate_sha256']);self.assertFalse(second['changes']['recipes']['changed'])
        self.data['snapshot']['game_version']='synthetic-v2.2';self.data['recipes'][0]['inputs'][0]['quantity']=4;self.write();self.assertFalse(self.run_import()['written']);r=self.run_import(allow_version_change=True);self.assertTrue(r['written']);self.assertIn('sample:make-part',r['changes']['recipes']['changed']);self.assertTrue((self.root/'.private'/r['backup']).is_file())
    def test_corrupt_previous_and_public_output_refused(self):
        p=self.root/'.private/catalog-v2-candidate.json';p.parent.mkdir();p.write_text('{}');r=self.run_import();self.assertFalse(r['written']);self.assertEqual(p.read_text(),'{}')
        with self.assertRaises(m.base.ImportFailure):self.run_import(output=self.root/'dist/catalog.json')
        with self.assertRaises(m.base.ImportFailure):self.run_import(output=self.source)
    def test_channel_changes_require_explicit_opt_in_and_records_cannot_mix(self):
        self.assertTrue(self.run_import()['written']);self.data['snapshot']['channel']='other-test';self.write();self.assertFalse(self.run_import()['written']);self.assertTrue(self.run_import(allow_version_change=True)['written']);self.data['items'][0]['channel']='wrong';self.assertTrue(m.validate(self.data)[0])
    def test_invalid_unknown_root_and_input_semantics_refused(self):
        v=copy.deepcopy(self.data);v['publication']={'status':'approved'};self.assertTrue(m.validate(v)[0]);self.data['recipes'][0]['inputs'][0]['options'][0]['kind']='guessed';self.assertTrue(m.validate(self.data)[0])
if __name__=='__main__':unittest.main()
