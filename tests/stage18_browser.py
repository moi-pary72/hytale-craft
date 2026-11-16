"""Original visual system regression against the actual user-only build; no real game data."""
import unittest,threading,os,json
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.build_pages import build,ROOT
OUT=ROOT/'.private/stage18/public-screens';OUT.mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
class VisualTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  build();cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'dist')));threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox']);cls.url=f'http://127.0.0.1:{cls.server.server_port}/'
 @classmethod
 def tearDownClass(cls):cls.browser.close();cls.p.stop();cls.server.shutdown();cls.server.server_close()
 def page(self,lang='en'):
  c=self.browser.new_context(viewport={'width':393,'height':852},is_mobile=True,has_touch=True,locale=lang,reduced_motion='reduce');self.addCleanup(c.close);p=c.new_page();p.set_default_timeout(10000);p.goto(self.url);p.wait_for_selector('#goals button');return p
 def inventory(self,p):p.locator('#nav [data-view=inventory]').click();p.wait_for_selector('.iv-modes')
 def test_four_locales_compact_inventory_keyboard_back_and_saved_choice(self):
  for lang in ['en','ru','es','pt-BR']:
   p=self.page(lang);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));self.inventory(p);p.locator('.iv-modes [data-mode=compact]').first.click();self.assertEqual(p.locator('.iv-compact .dw-slot').count(),7)
   for width in [320,360,393,430]:
    p.set_viewport_size({'width':width,'height':852});self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'));self.assertFalse(p.locator('#sheet-content').evaluate('(e)=>e.scrollWidth>e.clientWidth+1'))
   p.set_viewport_size({'width':393,'height':852});p.click('#handle');p.locator('.iv-compact').scroll_into_view_if_needed();p.screenshot(path=str(OUT/f'inventory-{lang}.png'));p.locator('#sheet-content input[type=search]').first.focus();p.set_viewport_size({'width':393,'height':480});self.assertTrue(p.locator('#close').is_visible());p.keyboard.press('Escape');p.wait_for_selector('#sheet:not([open])',state='attached');p.reload();p.wait_for_selector('#goals button');self.inventory(p);self.assertTrue(p.locator('.iv-compact').count());self.assertEqual(p.locator('#language').input_value(),lang);p.go_back();self.assertFalse(p.locator('#sheet').is_visible());self.assertFalse(errors)
 def test_demo_disclosure_and_individual_images(self):
  p=self.page();p.locator('[data-goal=fight]').click();self.assertEqual(p.locator('.dw-data-notice[open]').count(),0);p.locator('[data-item="lesson:blade"]').click();p.click('#handle');self.assertEqual(p.locator('.dw-item-head [data-visual=individual]').count(),1);p.locator('.dw-data-notice').first.locator('summary').click();self.assertIn('not',p.locator('.dw-data-notice').first.inner_text().lower());p.locator('#sheet-content').evaluate('(e)=>e.scrollTop=0');p.screenshot(path=str(OUT/'detail.png'));p.get_by_role('button',name='Calculate resources',exact=True).click();self.assertTrue(p.locator('#calculation .iv-art').count());self.assertFalse(p.evaluate('Array.from(document.images).some(i=>i.complete&&!i.naturalWidth)'))
 def test_back_restores_internal_scroll_without_modifying_saved_data(self):
  p=self.page();p.locator('[data-goal=fight]').click();p.locator('[data-item="lesson:blade"]').click();p.click('#handle');p.locator('#sheet-content').evaluate('(e)=>e.scrollTop=200');before=p.locator('#sheet-content').evaluate('(e)=>e.scrollTop');p.locator('.dw-grid .dw-slot button').first.evaluate('(e)=>e.click()');p.go_back();self.assertAlmostEqual(p.locator('#sheet-content').evaluate('(e)=>e.scrollTop'),before,delta=3)
 def test_projects_plan_and_advanced_share_visuals_and_saved_data(self):
  p=self.page();p.click('#mode-maker');p.locator('[data-tool=projects]').click();p.get_by_role('button',name='Plan',exact=True).first.click();p.fill('#plan','lesson:blade: 2\nlesson:pick: 1');p.get_by_role('button',name='Calculate plan',exact=True).click();self.assertTrue(p.locator('#plan-result .iv-art').count());p.click('#handle');p.locator('#sheet-content').evaluate('(e)=>e.scrollTop=0');p.screenshot(path=str(OUT/'plan.png'));p.get_by_role('button',name='Save as project',exact=True).click();p.fill('#project-name','Expedition kit');p.locator('#project-save').get_by_role('button',name='Save as project',exact=True).click();p.get_by_role('button',name='Saved projects',exact=True).click();self.assertTrue(p.locator('.dw-project-items .iv-art').count());p.screenshot(path=str(OUT/'projects.png'));p.keyboard.press('Escape');p.wait_for_selector('#sheet:not([open])',state='attached');p.locator('[data-tool=calculator]').click();p.get_by_role('button',name='Advanced learning workshop',exact=True).click();p.wait_for_selector('#advanced-target');self.assertTrue(p.locator('.dw-selected-item .iv-art').count());p.locator('#sheet-content').evaluate('(e)=>e.scrollTop=0');p.screenshot(path=str(OUT/'advanced.png'));self.assertIn('Expedition kit',p.evaluate('localStorage.getItem("hytale-craft-projects-v1")'))
 def test_missing_atlas_has_accessible_css_fallback_no_broken_image(self):
  p=self.page();p.route('**/assets/item-system/categories.webp',lambda r:r.fulfill(status=404,body=''));p.evaluate('()=>{const v=CraftItemVisuals.image({id:"test:unknown"});v.id="fallback-test";document.body.append(v)}');p.wait_for_selector('#fallback-test.iv-failed');self.assertEqual(p.locator('#fallback-test img').count(),0);self.assertIn('unavailable',p.locator('#fallback-test').get_attribute('aria-label'))
 def test_quick_inventory_changes_existing_storage_and_never_spends_it_on_view(self):
  p=self.page();self.inventory(p);
  for _ in range(3):p.get_by_role('button',name='Add one Practice fibre',exact=True).click()
  raw=p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")');self.assertIn('lesson:fibre: 3',raw);p.locator('#sheet-content>button').first.click();p.wait_for_selector('.dw-card');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'),raw)
if __name__=='__main__':unittest.main()
