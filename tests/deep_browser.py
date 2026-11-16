"""Deep workshop: real production-allowlisted build, not mocked DOM."""
import unittest,threading,json,time,os,importlib.util
from functools import partial
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'.private/deep-workshop';OUT.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
class DeepTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  spec=importlib.util.spec_from_file_location('b',ROOT/'scripts/build_pages.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.build()
  cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'dist')));threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.url=f'http://127.0.0.1:{cls.server.server_port}/';cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox'])
 @classmethod
 def tearDownClass(cls):cls.browser.close();cls.p.stop();cls.server.shutdown();cls.server.server_close()
 def page(self,lang='en',inventory='lesson:fibre: 3\nlesson:stone: 4\nlesson:wood: 3'):
  c=self.browser.new_context(viewport={'width':393,'height':852},is_mobile=True,has_touch=True,locale=lang,reduced_motion='reduce');self.addCleanup(c.close);c.add_init_script('if(localStorage.getItem("hytale-craft-inventory-v1")===null)localStorage.setItem("hytale-craft-inventory-v1",'+json.dumps(inventory)+');');p=c.new_page();p.set_default_timeout(10000);p.goto(self.url);p.wait_for_selector('#goals button');return p
 def open(self,p):
  p.locator(('#sheet-nav' if p.locator('#sheet').is_visible() else '#nav')+' [data-view=inventory]').click();p.locator('#sheet-content>button').first.click();p.wait_for_selector('.dw-card')
 def test_four_languages_four_mobile_widths(self):
  labels={'en':'What can I craft?','ru':'Что я могу скрафтить?','es':'¿Qué puedo fabricar?','pt-BR':'O que posso fabricar?'}
  for lang,label in labels.items():
   p=self.page(lang);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));self.open(p);self.assertEqual(p.locator('#sheet-title').inner_text(),label);p.click('#handle')
   for width in [320,360,393,430]:
    p.set_viewport_size({'width':width,'height':852});self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'));self.assertFalse(p.locator('#sheet-content').evaluate('(e)=>e.scrollWidth>e.clientWidth+1'))
   p.set_viewport_size({'width':393,'height':852});p.screenshot(path=str(OUT/f'craftable-{lang}.png'));self.assertFalse(errors)
 def test_independent_vs_shared_inventory_and_persistence(self):
  p=self.page();self.open(p);self.assertEqual(p.locator('[data-craftable]').count(),4)
  for id in ['lesson:blade','lesson:pick']:
   p.locator('[data-craftable="'+id+'"]').get_by_role('button',name='Add to preview',exact=True).click();p.wait_for_timeout(80)
  self.assertIn('compete for materials',p.locator('#sheet-content').inner_text());self.assertIn('lesson:fibre: 3',p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'))
  p.locator('#sheet-content>details').filter(has=p.locator('input[type=search]')).first.locator('summary').first.click();p.get_by_role('button',name='Add one Practice fibre',exact=True).click();p.wait_for_timeout(80);self.assertIn('lesson:fibre: 4',p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'))
  p.reload();p.wait_for_selector('#goals button');self.open(p);self.assertIn('lesson:fibre: 4',p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'))

 def test_detail_raw_used_in_back_and_keyboard(self):
  p=self.page();p.locator('[data-goal=fight]').click();p.locator('[data-item="lesson:blade"]').click();p.click('#handle');self.assertTrue(p.locator('.dw-item-head').is_visible());p.locator('#sheet-content').evaluate('(e)=>e.scrollTop=0');p.screenshot(path=str(OUT/'detail-top-en.png'));p.get_by_text('Craft path',exact=True).click();self.assertIn('Practice binding strip',p.locator('#sheet-content').inner_text());p.screenshot(path=str(OUT/'detail-en.png'))
  p.locator('.dw-grid .dw-slot').first.get_by_role('button',name='Inspect',exact=True).click();self.assertIn('Used in',p.locator('#sheet-content').inner_text());p.go_back();self.assertIn('Practice blade',p.locator('#sheet-title').inner_text());p.keyboard.press('Tab');self.assertTrue(p.evaluate('document.getElementById("sheet").contains(document.activeElement)'));p.keyboard.press('Escape');p.wait_for_selector('#sheet:not([open])',state='attached')
 def test_broken_inventory_preserved(self):
  p=self.page(inventory='broken: nope');p.locator('#nav [data-view=inventory]').click();p.locator('#sheet-content>button').first.click();p.wait_for_selector('.dw-empty');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'),'broken: nope');self.assertFalse(p.locator('.dw-card').count())
 def test_standalone_empty_state_and_images_need_no_subrequests(self):
  import subprocess
  subprocess.run(['python3','scripts/export_beta.py','--output',str(OUT/'preview.html')],cwd=ROOT,check=True,capture_output=True)
  p=self.page(inventory='');requests=[];p.on('request',lambda r:requests.append(r.url));p.route('**/deep-offline.html',lambda r:r.fulfill(status=200,content_type='text/html',body=(OUT/'preview.html').read_text()));p.goto(self.url+'deep-offline.html');p.wait_for_selector('#goals button');p.locator('#nav [data-view=inventory]').click();p.locator('#sheet-content>button').first.click();p.wait_for_selector('.dw-empty');p.locator('.dw-empty img').scroll_into_view_if_needed();p.locator('.dw-empty img').evaluate('(e)=>e.decode()');p.wait_for_timeout(100);self.assertEqual(len(requests),1,requests)
 def test_long_user_item_and_station_are_safe_and_wrap(self):
  p=self.page();id='Own-'+('x'*95);source='<img src=x onerror=alert(1)>';data={id:{'yield':1,'source':source,'ingredients':{'Raw':2},'workstations':['F'*100]}};p.evaluate('(d)=>localStorage.setItem("hytale-craft-recipes-v1",JSON.stringify(d))',data);p.reload();p.wait_for_selector('#goals button');p.click('#mode-maker');p.locator('[data-tool=calculator]').click();p.select_option('#scope','user');p.locator('[data-item]').click();p.set_viewport_size({'width':320,'height':852});self.assertFalse(p.locator('#sheet-content').evaluate('(e)=>e.scrollWidth>e.clientWidth+1'));self.assertEqual(p.locator('#sheet-content img[onerror]').count(),0);self.assertEqual(p.locator('#sheet-title').inner_text(),id)
if __name__=='__main__':unittest.main()
