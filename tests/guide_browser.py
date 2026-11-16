"""Public mobile guide regression; original examples and synthetic user data only."""
import unittest,threading,os,json
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.build_pages import build,ROOT
class Guide(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  build(guide=True);cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(ROOT/'dist')));threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox'])
 @classmethod
 def tearDownClass(cls):cls.browser.close();cls.p.stop();cls.server.shutdown();cls.server.server_close()
 def test_guide_search_item_back_and_large_user_recipe(self):
  for lang in ['en','ru','es','pt-BR']:
   ctx=self.browser.new_context(viewport={'width':393,'height':852},locale=lang,reduced_motion='reduce');p=ctx.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{self.server.server_port}');p.wait_for_selector('#guide-search');(ROOT/'.private/mobile-guide').mkdir(exist_ok=True);p.screenshot(path=str(ROOT/'.private/mobile-guide'/('home-'+lang+'.png')));p.fill('#guide-search','lesson:blade');p.locator('#guide-home [data-item="lesson:blade"]').click();p.wait_for_selector('.dw-item-head');p.screenshot(path=str(ROOT/'.private/mobile-guide'/('item-'+lang+'.png')));self.assertIn('#item=',p.url);self.assertFalse(p.locator('#quantity').count());self.assertEqual(p.locator('#sheet').evaluate('(e)=>e.matches(":modal")'),False)
   for width in [320,360,393,430]:
    p.set_viewport_size({'width':width,'height':852});self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'));self.assertEqual(p.locator('#sheet-content').evaluate('(e)=>getComputedStyle(e).overflowY'),'visible')
   p.locator('.dw-grid button').first.click();p.go_back();p.wait_for_selector('.dw-item-head');p.go_back();p.wait_for_selector('#guide-search');self.assertEqual(p.locator('#guide-search').input_value(),'lesson:blade');self.assertFalse(errors);ctx.close()
  ctx=self.browser.new_context(viewport={'width':320,'height':700});p=ctx.new_page();p.goto(f'http://127.0.0.1:{self.server.server_port}');p.wait_for_selector('#guide-search');data={'Large own recipe':{'yield':2,'source':'Synthetic test only','ingredients':{'Long material '+str(i):i+1 for i in range(50)}}};raw=json.dumps(data);p.evaluate('(v)=>{localStorage.setItem("hytale-craft-recipes-v1",v);localStorage.setItem("hytale-craft-inventory-v1","retired:item: 9")}',raw);p.reload();p.wait_for_selector('#guide-search');p.fill('#guide-search','Large own recipe');p.locator('#guide-home [data-item]').click();self.assertEqual(p.locator('.dw-grid>.dw-slot').count(),50);self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'));self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-recipes-v1")'),raw);self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'),'retired:item: 9');ctx.close()
if __name__=='__main__':unittest.main()
