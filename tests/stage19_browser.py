"""Owner Android-file preview and private visual activation, original/synthetic data only."""
import unittest,json,hashlib,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import real_lab_browser as lab
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'.private/stage19/safe-screens';OUT.mkdir(parents=True,exist_ok=True)
class Stage19Browser(lab.ResearchBrowser):
 def test_research_visuals_bind_only_to_private_matching_source(self):
  p=self.page();folder=Path(self.tmp.name)/'build';cfg=json.loads((folder/'lab-config.js').read_text().split('=',1)[1].rstrip(';\n'));revision=json.loads((folder/'research-data.json').read_text())['canonical']['snapshot']['source_revision'];manifest={'mode':'private-research','source_revision':revision,'entries':[{'item_id':'test:gear','path':'research-art/items.webp','columns':3,'tile':0,'reference':{'reference_url':'https://example.invalid/item-image','reference_page':'https://example.invalid/item','reference_version':'synthetic-test','silhouette':'Invented example','publication':'private-research-only; underlying game-design rights unconfirmed'}}]};raw=json.dumps(manifest).encode();cfg['visualsSha256']=hashlib.sha256(raw).hexdigest();p.route('**/lab-config.js',lambda r:r.fulfill(body='window.CRAFT_LAB='+json.dumps(cfg)+';'));p.route('**/research-visuals.json',lambda r:r.fulfill(body=raw,content_type='application/json'));p.route('**/research-art/items.webp',lambda r:r.fulfill(body=(ROOT/'assets/item-system/extended.webp').read_bytes(),content_type='image/webp'));self.ready(p);self.assertFalse(p.locator('#lab-interpretations').is_checked());p.check('#lab-interpretations');p.fill('#lab-search','Synthetic gear');p.locator('.lab-card').click();self.assertGreaterEqual(p.locator('#sheet-content [data-research=true]').count(),1);p.get_by_text('Visual evidence · original interpretation, not official art',exact=True).click();self.assertIn('synthetic-test',p.locator('#sheet-content').inner_text());p.keyboard.press('Escape');before=p.evaluate('localStorage.getItem("hytale-craft-lab-inventory-v1")');p.click('#lab-detach');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-lab-inventory-v1")'),before);self.assertFalse(p.evaluate('!!CraftItemVisuals.researchEvidence("test:gear")'))
 def test_corrupt_optional_visual_metadata_does_not_break_catalogue(self):
  p=self.page();folder=Path(self.tmp.name)/'build';cfg=json.loads((folder/'lab-config.js').read_text().split('=',1)[1].rstrip(';\n'));cfg['visualsSha256']='0'*64;p.route('**/lab-config.js',lambda r:r.fulfill(body='window.CRAFT_LAB='+json.dumps(cfg)+';'));p.route('**/research-visuals.json',lambda r:r.fulfill(body='{}',content_type='application/json'));self.ready(p);self.assertEqual(p.locator('.lab-card').count(),24);self.assertEqual(p.locator('#lab-interpretations').count(),0);self.assertIn('checksum',p.evaluate('CRAFT_LAB_VISUAL_WARNING'))
# Do not inherit/repeat the4existing source tests; CI runs their file separately.
for name in list(lab.ResearchBrowser.__dict__):
 if name.startswith('test_'):setattr(Stage19Browser,name,None)
class OwnerFilePreview(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  import threading
  from functools import partial
  from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
  class Quiet(SimpleHTTPRequestHandler):
   def log_message(self,*a):pass
  cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(OUT)));threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.url=f'http://127.0.0.1:{cls.server.server_port}/owner-preview.html'
 @classmethod
 def tearDownClass(cls):cls.server.shutdown();cls.server.server_close()
 def test_file_origin_when_browser_policy_allows(self):
  import subprocess
  subprocess.run(['python3','scripts/export_owner_preview.py','--output',str(OUT/'owner-preview.html')],cwd=ROOT,check=True,capture_output=True)
  with sync_playwright()as pw:
   browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox']);page=browser.new_page()
   try:page.goto((OUT/'owner-preview.html').as_uri());page.wait_for_selector('#goals button')
   except Exception as error:
    if 'ERR_BLOCKED_BY_ADMINISTRATOR' in str(error):self.skipTest('Managed browser blocks file URLs; no policy bypass. Exact HTML is tested over loopback separately.')
    raise
   finally:browser.close()

 def test_actual_single_file_four_locales_mobile_persistence_and_calculation(self):
  import subprocess
  subprocess.run(['python3','scripts/export_owner_preview.py','--output',str(OUT/'owner-preview.html')],cwd=ROOT,check=True,capture_output=True)
  with sync_playwright()as pw:
   browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox']);context=browser.new_context(viewport={'width':393,'height':852},is_mobile=True,has_touch=True,reduced_motion='reduce');p=context.new_page();p.set_default_timeout(10000);errors=[];requests=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:requests.append(r.url));p.goto(self.url);p.wait_for_selector('#goals button');self.assertEqual(p.locator('#goals button').count(),10)
   for lang in ['en','ru','es','pt-BR']:p.select_option('#language',lang);p.wait_for_function('(lang)=>document.documentElement.lang===lang',arg=lang)
   p.select_option('#language','en');p.wait_for_function('document.documentElement.lang==="en"');p.locator('#nav [data-view=more]').click();p.get_by_role('button',name='Visual gallery',exact=True).click();p.wait_for_selector('[data-gallery]');self.assertEqual(p.locator('[data-gallery]').count(),24);p.locator('[data-gallery=bow]').click();self.assertIn('not an official',p.locator('#sheet-content').inner_text());p.keyboard.press('Escape');p.wait_for_selector('#sheet:not([open])',state='attached');p.locator('[data-goal=fight]').click();p.locator('[data-item="lesson:blade"]').click();p.fill('#quantity','2');p.get_by_role('button',name='Calculate resources',exact=True).click();self.assertIn('Practice',p.locator('#calculation').inner_text())
   for width in [320,360,393,430]:p.set_viewport_size({'width':width,'height':852});self.assertFalse(p.locator('#sheet-content').evaluate('(e)=>e.scrollWidth>e.clientWidth+1'))
   p.set_viewport_size({'width':393,'height':852});p.click('#handle');p.locator('#sheet-content').evaluate('(e)=>e.scrollTop=0');p.screenshot(path=str(OUT/'interactive-file.png'));p.keyboard.press('Escape');p.wait_for_selector('#sheet:not([open])',state='attached');p.locator('#nav [data-view=inventory]').click();p.get_by_role('button',name='Add one Practice fibre',exact=True).click();before=p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")');p.reload();p.wait_for_selector('#goals button');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'),before);self.assertEqual(p.locator('#language').input_value(),'en');self.assertFalse(errors);self.assertTrue(all(url==self.url or url.startswith('data:')for url in requests),requests);context.close();browser.close()
if __name__=='__main__':unittest.main()
