"""Public CI tests use only invented local export fixtures, never network/game data."""
import unittest,tempfile,json,threading,os,importlib.util,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.build_real_data_lab import ROOT,build
from scripts.serve_real_data_lab import make_server
spec=importlib.util.spec_from_file_location('synthetic_export',ROOT/'tests/helpers/research-export.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class ResearchBrowser(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory(dir=ROOT/'.private');folder=Path(cls.tmp.name);inp=folder/'input';inp.mkdir();m,i,r=module.export_fixture()
  for n in range(116):i['items'].append({'id':f'test:z-{n:03}','name':f'Synthetic extra {n}','category':'synthetic'})
  i['count']=len(i['items']);m['datasets'][0]['recordCount']=i['count']
  for name,v in [('manifest',m),('items',i),('recipes',r)]:(inp/(name+'.json')).write_text(json.dumps(v))
  build(inp,folder/'build',True);cls.server=make_server(folder/'build');threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.url=f'http://127.0.0.1:{cls.server.server_port}/';cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox'])
 @classmethod
 def tearDownClass(cls):cls.browser.close();cls.p.stop();cls.server.shutdown();cls.server.server_close();cls.tmp.cleanup()
 def page(self):
  c=self.browser.new_context(viewport={'width':393,'height':852},is_mobile=True,has_touch=True,reduced_motion='reduce');self.addCleanup(c.close);p=c.new_page();p.set_default_timeout(10000);return p
 def ready(self,p):p.goto(self.url);p.wait_for_selector('.lab-card')
 def test_search_samples_mobile_sheets_back(self):
  p=self.page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));self.ready(p);self.assertEqual(p.locator('.lab-card').count(),24);p.select_option('#lab-size','100');self.assertIn('100 matching items',p.locator('#view-content').inner_text());p.select_option('#lab-size','10000');self.assertIn('120 matching items',p.locator('#view-content').inner_text())
  p.fill('#lab-search','Synthetic gear');p.locator('.lab-card').click();p.fill('#lab-quantity','2');p.get_by_role('button',name='Calculate materials',exact=True).click();self.assertIn('Synthetic raw',p.locator('#lab-calculation').inner_text())
  for w in [320,360,393,430]:p.set_viewport_size({'width':w,'height':852});self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'));self.assertFalse(p.locator('#sheet-content').evaluate('(e)=>e.scrollWidth>e.clientWidth+1'))
  p.go_back();self.assertFalse(p.locator('#sheet').is_visible());self.assertFalse(errors)
 def test_inventory_plan_and_discovery_share_storage(self):
  p=self.page();self.ready(p);p.evaluate('localStorage.setItem("hytale-craft-lab-inventory-v1",JSON.stringify({"test:raw":6}))');p.reload();p.wait_for_selector('.lab-card');p.locator('#nav [data-view=craftable]').click();p.wait_for_function('document.querySelector("#view-content").textContent.includes("material-feasible")');p.wait_for_selector('#view-content .dw-card');self.assertIn('Maximum independently',p.locator('#view-content').inner_text());before=p.evaluate('localStorage.getItem("hytale-craft-lab-inventory-v1")');p.get_by_role('button',name='Add one to shared plan').first.click();p.locator('#nav [data-view=plan]').click();p.get_by_role('button',name='Calculate shared plan',exact=True).click();self.assertIn('Materials remaining',p.locator('#lab-plan-result').inner_text());self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-lab-inventory-v1")'),before)
 def test_corrupt_payload_is_blocked(self):
  p=self.page();p.route('**/research-data.json',lambda r:r.fulfill(status=200,content_type='application/json',body='{}'));p.goto(self.url);p.wait_for_function('document.getElementById("lab-error").textContent.includes("checksum")');self.assertEqual(p.locator('.lab-card').count(),0)
if __name__=='__main__':unittest.main()
