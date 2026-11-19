"""Own original icons, no repeated warning, real source-backed partial pickaxe composition."""
import unittest
import guide_browser as base
class Art(base.Guide):
 test_guide_search_item_back_and_large_user_recipe=None
 def test_original_art_and_pickaxe_mobile(self):
  out=base.ROOT/'.private/item-art-release/screens';out.mkdir(parents=True,exist_ok=True)
  for lang in ['en','ru','es','pt-BR']:
   c=self.browser.new_context(viewport={'width':393,'height':852},locale=lang,reduced_motion='reduce');p=c.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{self.server.server_port}/');p.wait_for_selector('#guide-search');self.assertEqual(p.locator('#goals button').count(),10);p.fill('#guide-search','Weapon_Sword_');self.assertEqual(p.locator('#guide-home [data-item]').count(),7);self.assertEqual(p.locator('#guide-home .iv-art[data-visual=interpretation]').count(),4);self.assertTrue(p.locator('#guide-home .iv-art').evaluate_all('(xs)=>xs.every(x=>["none","normal"].includes(getComputedStyle(x,"::after").content))'));p.screenshot(path=str(out/f'swords-{lang}.png'))
   p.fill('#guide-search','Weapon_Longsword_');self.assertEqual(p.locator('#guide-home [data-item]').count(),6);self.assertEqual(p.locator('#guide-home .iv-art[data-visual=interpretation]').count(),5);self.assertEqual(p.locator('#guide-home .iv-art[data-visual=interpretation] img').evaluate_all('(xs)=>xs.filter(x=>x.getAttribute("src").endsWith("weapon-variants-additions.webp")).length'),1);self.assertEqual(p.locator('#guide-home .iv-art[data-visual=interpretation] img').evaluate_all('(xs)=>xs.filter(x=>x.getAttribute("src").endsWith("weapon-variants.webp")).length'),4);p.locator('#guide-home .iv-art[data-visual=interpretation] img').first.scroll_into_view_if_needed();p.wait_for_function('Array.from(document.querySelectorAll("#guide-home .iv-art[data-visual=interpretation] img")).every(x=>x.complete && x.naturalWidth>0)');p.screenshot(path=str(out/f'longswords-{lang}.png'))
   p.fill('#guide-search','Tool_Pickaxe_Iron');p.locator('#guide-home [data-item=Tool_Pickaxe_Iron]').click();p.wait_for_selector('.dw-grid');self.assertEqual(p.locator('.dw-grid .dw-slot').count(),3);self.assertEqual(p.locator('.dw-grid .dw-slot>span:not(.iv-art)').all_text_contents(),['× 5','× 2','× 2']);self.assertFalse(p.locator('#sheet-content>.dw-panel').first.locator('.muted').filter(has_text='official').count());self.assertIn('materials.webp',p.locator('#sheet-content>.dw-panel').first.locator('img').get_attribute('src'));p.locator('#craft-path>summary').click();p.wait_for_selector('#craft-path[open] .craft-path-step');self.assertEqual(p.locator('#craft-path .craft-path-step').count(),6)
   for width in [320,360,393,430]:p.set_viewport_size({'width':width,'height':852});self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'))
   p.set_viewport_size({'width':393,'height':852});p.screenshot(path=str(out/f'pickaxe-{lang}.png'),full_page=True);self.assertFalse(p.evaluate('[...document.images].some(i=>i.complete&&!i.naturalWidth)'));p.locator('.dw-grid button').first.click();p.go_back();p.wait_for_selector('#craft-path[open]');self.assertFalse(errors);c.close()
 def test_weapon_atlas_crop_cards_compact_and_detail(self):
  """Regression for the 100px guide img cap which exposed unrelated rows of every 4x4 atlas."""
  out=base.ROOT/'.private/stage18/public-screens';out.mkdir(parents=True,exist_ok=True) # CI uploads this existing screenshot directory
  cases=(
   ('Weapon_Battleaxe_Iron','battleaxe','materials.webp'),
   ('Weapon_Daggers_Iron','dagger','weapon-variants.webp'),
   ('Weapon_Mace_Thorium','mace','weapon-variants-additions.webp'),
   ('Weapon_Shield_Iron','shield','weapon-variants.webp'),
   # Category-level fallback must still show the right silhouette, not neighboring atlas cells.
   ('Tool_Hatchet_Iron','axe','categories.webp'),
   ('Weapon_Daggers_Bronze','dagger','extended.webp'),
   ('Weapon_Mace_Mithril','mace','crafting.webp'),
   ('Weapon_Spear_Bronze','spear','crafting.webp'),
  )
  for lang in ('en','ru'):
   c=self.browser.new_context(viewport={'width':393,'height':852},locale=lang,reduced_motion='reduce')
   p=c.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   try:
    p.goto(f'http://127.0.0.1:{self.server.server_port}/')
    p.wait_for_selector('#guide-search')
    def check_crop(icon):
     img=icon.locator('img')
     self.assertTrue(img.evaluate('im=>im.complete && im.naturalWidth===1024 && im.naturalHeight===1024'))
     dimensions=img.evaluate('im=>{const p=im.parentElement.getBoundingClientRect(),r=im.getBoundingClientRect(),s=getComputedStyle(im);return {max:s.maxHeight,w:r.width/p.width,h:r.height/p.height,square:Math.abs(p.width-p.height)<2}}')
     self.assertEqual(dimensions['max'],'none')
     self.assertTrue(dimensions['square'],dimensions)
     self.assertGreater(dimensions['w'],3.7,dimensions)
     self.assertLess(dimensions['w'],4.1,dimensions)
     self.assertGreater(dimensions['h'],3.7,dimensions)
     self.assertLess(dimensions['h'],4.1,dimensions)
    for ident,family,atlas in cases:
     p.fill('#guide-search',ident)
     icon=p.locator(f'#guide-home [data-item="{ident}"] .iv-art.iv-sprite')
     icon.wait_for()
     self.assertEqual(icon.get_attribute('data-family'),family)
     self.assertTrue(icon.locator('img').get_attribute('src').endswith(atlas))
     p.wait_for_function('(id)=>{const im=document.querySelector("#guide-home [data-item="+JSON.stringify(id)+"] .iv-art.iv-sprite>img");return im?.complete&&im.naturalWidth===1024}',arg=ident)
     check_crop(icon)
     if ident in ('Tool_Hatchet_Iron','Weapon_Daggers_Bronze','Weapon_Mace_Mithril','Weapon_Spear_Bronze'):
      self.assertEqual(icon.get_attribute('data-visual'),'category')
      marker=icon.evaluate('el=>({content:getComputedStyle(el,"::before").content,color:getComputedStyle(el,"::before").backgroundColor})')
      self.assertNotEqual(marker['content'],'none',marker)
      self.assertNotEqual(marker['color'],'rgba(0, 0, 0, 0)',marker)
    p.fill('#guide-search','Weapon_Daggers_Iron')
    icon=p.locator('#guide-home [data-item="Weapon_Daggers_Iron"] .iv-art.iv-sprite')
    for width in (320,360,393,430):
     p.set_viewport_size({'width':width,'height':852})
     self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'))
     check_crop(icon)
     p.screenshot(path=str(out/f'art33-{lang}-cards-{width}.png'),full_page=True)
     p.locator('#guide-home .iv-modes button[data-mode=compact]').click()
     self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'))
     check_crop(icon)
     p.screenshot(path=str(out/f'art33-{lang}-compact-{width}.png'),full_page=True)
     p.locator('#guide-home .iv-modes button[data-mode=cards]').click()
    p.locator('#guide-home [data-item="Weapon_Daggers_Iron"]').click()
    detail=p.locator('#sheet-content .iv-art.iv-sprite').first
    detail.wait_for()
    check_crop(detail)
    p.set_viewport_size({'width':393,'height':852})
    p.screenshot(path=str(out/f'art33-{lang}-detail-393.png'),full_page=True)
    self.assertFalse(errors)
   finally:c.close()

if __name__=='__main__':unittest.main()
