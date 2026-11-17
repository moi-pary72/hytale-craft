"""Public identity-only browsing: truthful missing recipes, source labels and mobile layout."""
import unittest
import guide_browser as base
class Identities(base.Guide):
 test_guide_search_item_back_and_large_user_recipe=None
 def test_item_identities_four_languages_mobile(self):
  out=base.ROOT/'.private/public-data-review/screens';out.mkdir(parents=True,exist_ok=True)
  for lang in ['en','ru','es','pt-BR']:
   c=self.browser.new_context(viewport={'width':393,'height':852},locale=lang,reduced_motion='reduce');p=c.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.add_init_script('localStorage.setItem("hytale-craft-inventory-v1","my:resource: 7")');p.goto(f'http://127.0.0.1:{self.server.server_port}');p.wait_for_selector('#guide-search');self.assertEqual(p.locator('#goals button').count(),10)
   for item in ['Weapon_Daggers_Adamantite','Armor_Cobalt_Hands','Tool_Pickaxe_Iron']:
    p.fill('#guide-search',item);p.locator('#guide-home [data-item="'+item+'"]').click();p.wait_for_selector('#craft-path');self.assertFalse(p.locator('.dw-grid').count());self.assertFalse(p.locator('#quantity').count());p.locator('#sheet-content details').filter(has=p.locator('a[target=_blank]')).locator('summary').click();self.assertIn('OpenHytale',p.locator('#sheet-content a[target=_blank]').inner_text());self.assertIn(item,p.locator('#sheet-content').inner_text())
    for width in [320,360,393,430]:p.set_viewport_size({'width':width,'height':852});self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'))
    if item=='Tool_Pickaxe_Iron':p.screenshot(path=str(out/f'pickaxe-{lang}.png'),full_page=True)
    p.go_back();p.wait_for_selector('#guide-search');self.assertEqual(p.locator('#guide-search').input_value(),item)
   self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'),'my:resource: 7');self.assertFalse(errors);c.close()
if __name__=='__main__':unittest.main()
