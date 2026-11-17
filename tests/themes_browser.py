import unittest,json
from guide_browser import Guide,ROOT
class Themes(Guide):
 def test_themes_routes_and_mobile(self):
  out=ROOT/'.private/themes';out.mkdir(exist_ok=True)
  for lang in ['en','ru','es','pt-BR']:
   c=self.browser.new_context(viewport={'width':393,'height':852},locale=lang,reduced_motion='reduce');p=c.new_page();p.set_default_timeout(12000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{self.server.server_port}');p.wait_for_selector('#goals button');self.assertEqual(p.locator('#goals button').count(),10)
   for width in [320,360,393,430]:
    p.set_viewport_size({'width':width,'height':852});self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'));self.assertTrue(p.locator('#goals .goal-label').evaluate_all('(xs)=>xs.every(x=>x.scrollWidth<=x.clientWidth+1)'))
   p.set_viewport_size({'width':393,'height':852});p.screenshot(path=str(out/f'home-{lang}-393.png'));p.locator('[data-goal=fight]').click();p.wait_for_selector('[data-subcategory]');p.screenshot(path=str(out/f'fight-{lang}-393.png'));p.locator('[data-subcategory=weapons]').click();p.fill('#theme-search','lesson:blade');p.select_option('#sheet-content select[aria-label]','complexity');p.locator('#sheet-content [data-item="lesson:blade"]').click();p.wait_for_selector('.dw-item-head');p.screenshot(path=str(out/f'item-{lang}-393.png'));p.go_back();p.wait_for_selector('#theme-search');self.assertEqual(p.locator('#theme-search').input_value(),'lesson:blade');self.assertEqual(p.locator('#sheet-content select[aria-label]').input_value(),'complexity');p.go_back();p.wait_for_selector('[data-subcategory]');p.go_back();p.wait_for_selector('#goals button');p.locator('[data-goal=defend]').click();p.wait_for_selector('[data-subcategory=helmets]');p.locator('[data-subcategory=helmets]').click();self.assertEqual(p.locator('#sheet-content [data-item=Armor_Iron_Head]').count(),1);p.screenshot(path=str(out/f'defend-{lang}-393.png'));self.assertFalse(errors);c.close()
if __name__=='__main__':unittest.main()
