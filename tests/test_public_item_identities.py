"""Own public factual selection; no private export or network used."""
import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from scripts import reference_publication as gate,prepare_public_item_identities as maker
class PublicIdentities(unittest.TestCase):
 def test_identities_do_not_assert_recipes_or_availability(self):
  data,a,_=gate.approved();self.assertEqual(len(data['items']),100);new=[i for i in data['items'].values() if i.get('source_name')=='OpenHytale API'];self.assertEqual(len(new),93)
  for row in new:self.assertIsNone(row['recipe']);self.assertEqual(row['availability'],'unknown');self.assertEqual(row['label_origin'],'derived-from-id');self.assertNotIn('item_level',row);self.assertNotIn('durability',row)
  self.assertEqual(sum(i['recipe'] is not None for i in data['items'].values()),4)
 def test_updated_hash_cannot_expand_scope_or_invent_fields(self):
  data,a,_=gate.approved();key=next(k for k,i in data['items'].items() if i.get('source_name')=='OpenHytale API')
  for mutation in ['count','stats','recipe','version']:
   v=copy.deepcopy(data)
   if mutation=='count':v['items'].pop(key)
   elif mutation=='stats':v['items'][key]['damage']=100
   elif mutation=='recipe':v['items'][key]['recipe']={'ingredients':{},'output_quantity':1}
   else:v['items'][key]['build']='current'
   with tempfile.TemporaryDirectory() as d:
    p=Path(d)/'data';p.mkdir();raw=json.dumps(v).encode();(p/'reference-selection.json').write_bytes(raw);approval=dict(a,sha256=hashlib.sha256(raw).hexdigest());(p/'reference-selection-approval.json').write_text(json.dumps(approval))
    with self.assertRaises(ValueError):gate.approved(Path(d))
 def test_changed_source_is_not_automatically_reapproved(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'changed.json';p.write_text('[]')
   with self.assertRaises(ValueError):maker.selection(p)
if __name__=='__main__':unittest.main()
