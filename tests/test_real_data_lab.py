import importlib.util,unittest,tempfile,json,copy,threading,http.client
from pathlib import Path
from scripts.build_real_data_lab import normalize,build,ROOT
from scripts.serve_real_data_lab import make_server
spec=importlib.util.spec_from_file_location('synthetic_export',ROOT/'tests/helpers/research-export.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class LabTests(unittest.TestCase):
 def setUp(self):self.m,self.i,self.r=module.export_fixture()
 def test_material_counts_multi_outputs_and_rights_remain_separate(self):
  x=normalize(self.m,self.i,self.r,{});self.assertEqual(len(x['canonical']['recipes']),2);self.assertEqual(x['meta']['metrics']['multi_output'],1);self.assertFalse(x['policy']['public_distribution']);self.assertEqual(x['canonical']['sources'][0]['license']['game_ip_use'],'unknown')
 def test_missing_selector_duplicate_output_and_placeholder_bench_quarantined(self):
  for kind in ['selector','duplicate','bench']:
   r=copy.deepcopy(self.r);row=r['recipes'][1]
   if kind=='selector':row['inputs']=[{'quantity':2}]
   if kind=='duplicate':row['outputs'].append(copy.deepcopy(row['outputs'][0]))
   if kind=='bench':row['benches']=[{'id':'TODO'}]
   x=normalize(self.m,self.i,r,{});self.assertEqual(len(x['canonical']['recipes']),1);self.assertIn('test:gear',x['meta']['blocked_items']);self.assertEqual(len(x['meta']['excluded']),1)
 def test_no_mixed_revisions_or_duplicate_ids(self):
  bad=copy.deepcopy(self.i);bad['extractedAt']='2026-01-02T00:00:00Z'
  with self.assertRaises(ValueError):normalize(self.m,bad,self.r,{})
  bad=copy.deepcopy(self.i);bad['items'][1]['id']=bad['items'][0]['id']
  with self.assertRaises(ValueError):normalize(self.m,bad,self.r,{})
 def test_build_is_opt_in_private_no_overwrite_and_loopback(self):
  (ROOT/'.private').mkdir(exist_ok=True)
  with tempfile.TemporaryDirectory(dir=ROOT/'.private') as td:
   folder=Path(td);inp=folder/'input';inp.mkdir()
   for name,value in zip(['manifest','items','recipes'],[self.m,self.i,self.r]):(inp/(name+'.json')).write_text(json.dumps(value))
   out=folder/'build'
   with self.assertRaises(ValueError):build(inp,out)
   report=build(inp,out,True);self.assertEqual(report['metrics']['items'],4);self.assertTrue((out/'research-data.json.gz').exists());server=make_server(out);self.assertEqual(server.server_address[0],'127.0.0.1');thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
   try:
    for headers,status in [({},200),({'Host':'attacker.invalid'},403),({'Origin':'https://attacker.invalid'},403)]:
     connection=http.client.HTTPConnection('127.0.0.1',server.server_port);connection.request('GET','/index.html',headers=headers);response=connection.getresponse();self.assertEqual(response.status,status);response.read();connection.close()
   finally:server.shutdown();server.server_close()
   with self.assertRaises(ValueError):build(inp,out,True)
   with self.assertRaises(ValueError):build(inp,ROOT/'dist/research-lab',True)
 def test_public_builder_keeps_research_viewer_and_inputs_outside_dist(self):
  from scripts import build_pages
  out=build_pages.build();self.assertFalse((out/'web/lab').exists());self.assertFalse((out/'research-data.json').exists());self.assertFalse((out/'lab-config.js').exists())
if __name__=='__main__':unittest.main()
