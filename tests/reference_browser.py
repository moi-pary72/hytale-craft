"""Two bounded factual references; never uses the private export."""
import unittest,json
import guide_browser as base
class Reference(base.Guide):
 test_guide_search_item_back_and_large_user_recipe=None
 def test_reference_items_four_languages(self):
  for lang in ['en','ru','es','pt-BR']:
   c=self.browser.new_context(viewport={'width':393,'height':852},locale=lang,reduced_motion='reduce');p=c.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{self.server.server_port}');p.wait_for_selector('#guide-search');p.fill('#guide-search','Weapon_Sword_Iron');p.locator('#guide-home [data-item=Weapon_Sword_Iron]').click();p.wait_for_selector('#sheet-content .dw-grid');self.assertEqual(p.locator('.dw-grid .dw-slot').count(),3);self.assertIn('6',p.locator('.dw-grid').inner_text());self.assertFalse(p.locator('#quantity').count());self.assertEqual(p.locator('#sheet-content a[target=_blank]').get_attribute('href'),'https://hytale.source.gs/items/iron-sword/')
   for width in [320,360,393,430]:p.set_viewport_size({'width':width,'height':852});self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'))
   p.locator('.dw-grid .dw-slot').first.click();p.wait_for_selector('#sheet-content .dw-panel');self.assertFalse(p.locator('.dw-grid').count());p.go_back();p.wait_for_selector('.dw-grid');self.assertEqual(p.locator('.dw-grid .dw-slot').count(),3);self.assertFalse(errors);c.close()
 def test_broken_source_preserves_other_features(self):
  c=self.browser.new_context();p=c.new_page();p.route('**/reference-data.json',lambda r:r.fulfill(status=200,content_type='application/json',body='{}'));p.add_init_script('localStorage.setItem("hytale-craft-inventory-v1","retired:item: 7")');p.goto(f'http://127.0.0.1:{self.server.server_port}');p.wait_for_selector('#guide-search');self.assertEqual(p.locator('#goals button').count(),10);self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'),'retired:item: 7');c.close()
 def test_user_id_collision_is_not_replaced(self):
  c=self.browser.new_context();p=c.new_page();raw=json.dumps({'Weapon_Sword_Iron':{'yield':3,'source':'My independently entered recipe','ingredients':{'Own raw':2}}});p.add_init_script('(function(){localStorage.setItem("hytale-craft-recipes-v1",'+json.dumps(raw)+');})()');p.goto(f'http://127.0.0.1:{self.server.server_port}');p.wait_for_selector('#guide-search');p.fill('#guide-search','Weapon_Sword_Iron');self.assertEqual(p.locator('#guide-home [data-item=Weapon_Sword_Iron]').count(),2);p.locator('#guide-home [data-item=Weapon_Sword_Iron][data-source=user]').click();self.assertIn('Own raw',p.locator('#sheet-content .dw-grid').inner_text());self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-recipes-v1")'),raw);self.assertFalse(p.locator('#sheet-content a[target=_blank]').count());c.close()
if __name__=='__main__':unittest.main()
