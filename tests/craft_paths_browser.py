"""Public bounded citations only; no restricted catalogue in screenshots or CI."""
import json,unittest,hashlib,time
import guide_browser as base
class Paths(base.Guide):
 test_guide_search_item_back_and_large_user_recipe=None
 def test_paths_mobile_languages_back_storage(self):
  (base.ROOT/'.private/stage23/screens').mkdir(parents=True,exist_ok=True)
  for lang in ['en','ru','es','pt-BR']:
   c=self.browser.new_context(viewport={'width':393,'height':852},locale=lang,reduced_motion='reduce');p=c.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   p.add_init_script('localStorage.setItem("hytale-craft-inventory-v1","my:resource: 7")')
   p.goto(f'http://127.0.0.1:{self.server.server_port}/#item=Weapon_Sword_Iron&source=reference&chain=1');p.wait_for_selector('#craft-path[open] .craft-path-step')
   self.assertEqual(p.locator('#craft-path .craft-path-step').count(),6)
   for width in [320,360,393,430]:
    p.set_viewport_size({'width':width,'height':852});self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'))
   p.set_viewport_size({'width':393,'height':852});p.screenshot(path=str(base.ROOT/'.private/stage23/screens'/f'path-{lang}.png'),full_page=True)
   p.locator('#craft-path .craft-path-step>button').nth(1).click();p.wait_for_selector('#craft-path');self.assertIn('Ingredient_Bar_Iron',p.url);p.go_back();p.wait_for_selector('#craft-path[open]');self.assertIn('Weapon_Sword_Iron',p.url)
   self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'),'my:resource: 7');self.assertFalse(errors);c.close()
 def test_home_ten_tiles_and_no_broken_images(self):
  c=self.browser.new_context(viewport={'width':393,'height':852});p=c.new_page();p.goto(f'http://127.0.0.1:{self.server.server_port}/');p.wait_for_selector('#guide-search');self.assertEqual(p.locator('#goals button').count(),10)
  p.screenshot(path=str(base.ROOT/'.private/stage23/screens/home-393.png'),full_page=True)
  self.assertFalse(p.evaluate('[...document.images].some(i=>i.complete&&!i.naturalWidth)'));c.close()
 def test_synthetic_5000_pagination_search_throttled(self):
  items={}
  for i in range(5000):
   items['synthetic:'+str(i)]={'id':'synthetic:'+str(i),'names':{'en':'Synthetic test item '+str(i)},'theme':'gather','subcategory':'ores','category':'materials','build':'synthetic','visual_family':'ore','recipe':None}
  raw=json.dumps({'items':items}).encode();config=(base.ROOT/'dist/web/build-config.js').read_text();config=config.replace(json.loads(config.split('=',1)[1].rstrip(';\n'))['referencesSha256'],hashlib.sha256(raw).hexdigest())
  c=self.browser.new_context(viewport={'width':320,'height':700});p=c.new_page();p.route('**/reference-data.json',lambda r:r.fulfill(body=raw,content_type='application/json'));p.route('**/web/build-config.js',lambda r:r.fulfill(body=config,content_type='text/javascript'));session=c.new_cdp_session(p);session.send('Emulation.setCPUThrottlingRate',{'rate':4});start=time.monotonic();p.goto(f'http://127.0.0.1:{self.server.server_port}/');p.wait_for_selector('#guide-search');p.fill('#guide-search','synthetic:4999');p.wait_for_selector('#guide-home [data-item="synthetic:4999"]');elapsed=time.monotonic()-start
  p.locator('[data-goal=gather]').click();p.locator('[data-subcategory=ores]').click();self.assertEqual(p.locator('#sheet-content .dw-catalog-card').count(),48);first=p.locator('#sheet-content .dw-catalog-card').first.get_attribute('data-item');p.locator('.lab-pager button').last.click();self.assertNotEqual(p.locator('#sheet-content .dw-catalog-card').first.get_attribute('data-item'),first);self.assertEqual(p.locator('#sheet-content .dw-catalog-card').count(),48);self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'));self.assertLess(elapsed,20)
  (base.ROOT/'.private/stage23/browser-scale.json').write_text(json.dumps({'synthetic_items':5000,'cpu_slowdown':4,'load_and_search_seconds':round(elapsed,3),'max_theme_cards':48,'physical_android':False}));c.close()
if __name__=='__main__':unittest.main()
