"""Canonical workshop through the same public UI, preserving all legacy keys."""
import json,unittest
from pathlib import Path
import beta_browser as beta
OUT=beta.ROOT/'.private/engine/screens';OUT.mkdir(parents=True,exist_ok=True)
class AdvancedTests(beta.BetaTests):
    def lab(self,p,ready=True):
        p.goto(self.url);p.wait_for_selector('#goals button');p.click('#mode-maker');p.locator('[data-tool=calculator]').click();p.locator('#sheet-content button').first.click();
        if ready:p.wait_for_selector('#advanced-plan')
    def close(self,p):p.keyboard.press('Escape');p.wait_for_selector('#sheet:not([open])',state='attached')
    def run_calc(self,p):p.locator('#sheet-content').get_by_role('button',name='Calculate resources',exact=True).click()
    def test_four_locales_all_widths_and_keyboard(self):
        for lang in ['en','ru','es','pt-BR']:
            p=self.page(lang);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));self.lab(p)
            for width in [320,360,393,430]:
                p.set_viewport_size({'width':width,'height':851});self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'));p.screenshot(path=str(OUT/f'lab-{lang}-{width}.png'))
            self.assertEqual(p.locator('html').get_attribute('lang'),lang)
            for _ in range(25):p.keyboard.press('Tab');self.assertTrue(p.locator('#sheet').evaluate('(e)=>e.contains(document.activeElement)'))
            self.assertFalse(errors,errors)
    def test_units_coproducts_requirements_inventory_and_legacy_storage(self):
        p=self.page();p.goto(self.url);p.wait_for_selector('#goals button');p.evaluate('''()=>{localStorage.setItem('hytale-craft-inventory-v1','sample:part: 2\\nsample:raw-a: 2\\nsample:raw-b: 1');localStorage.setItem('hytale-craft-recipes-v1',JSON.stringify({Own:{yield:1,source:'Original test',ingredients:{Raw:2}}}));localStorage.setItem('hytale-craft-projects-v1','[]');}''');before=p.evaluate('()=>[localStorage.getItem("hytale-craft-recipes-v1"),localStorage.getItem("hytale-craft-projects-v1"),localStorage.getItem("hytale-craft-inventory-v1")]');self.lab(p)
        p.fill('#advanced-quantity','2');p.get_by_role('button',name='Set quantity in plan',exact=True).click();p.get_by_role('button',name='Set quantity in plan',exact=True).click();self.assertEqual(p.locator('#advanced-plan').input_value(),'sample:device: 2');p.fill('#advanced-plan','sample:device: 1');p.fill('#advanced-level','2');p.fill('#advanced-memories','2');p.check('#advanced-known');p.check('#advanced-strict');self.run_calc(p);self.assertIn('Practice residue',p.locator('#advanced-result').inner_text());self.assertIn('Available',p.locator('#advanced-result').inner_text());self.assertIn('Practice material B',p.locator('#advanced-result').inner_text());self.assertEqual(p.evaluate('()=>[localStorage.getItem("hytale-craft-recipes-v1"),localStorage.getItem("hytale-craft-projects-v1"),localStorage.getItem("hytale-craft-inventory-v1")]'),before)
        p.get_by_role('button',name='My inventory',exact=True).click();p.go_back();p.wait_for_selector('#advanced-plan');self.assertEqual(p.locator('#advanced-level').input_value(),'2');p.reload();p.wait_for_selector('#advanced-plan');self.run_calc(p);self.assertIn('Practice residue',p.locator('#advanced-result').inner_text());self.close(p);p.click('#mode-seeker');self.open(p);self.assertEqual(p.locator('[data-item]').count(),1)
    def test_salvage_opt_in_does_not_mutate_saved_inventory(self):
        p=self.page();self.lab(p);p.evaluate('localStorage.setItem("hytale-craft-inventory-v1","sample:device: 1")');p.select_option('#advanced-target','sample:part');p.select_option('#advanced-recipe','sample:recycle-device');p.fill('#advanced-plan','sample:part: 1');self.run_calc(p);self.assertIn('Enable dismantling',p.locator('#notice').inner_text());p.check('#advanced-salvage');self.run_calc(p);self.assertIn('Dismantle gadget',p.locator('#advanced-result').inner_text());self.assertEqual(p.locator('#notice').inner_text(),'');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'),'sample:device: 1');p.reload();p.wait_for_selector('#advanced-plan');self.assertTrue(p.locator('#advanced-salvage').is_checked())
    def test_damaged_or_unapproved_payload_keeps_legacy_calculator_working(self):
        p=self.page();p.route('**/web/beta/advanced-data.json',lambda r:r.fulfill(status=200,content_type='application/json',body='{}'));p.goto(self.url);p.wait_for_selector('#goals button');p.click('#mode-maker');p.locator('[data-tool=calculator]').click();p.locator('#sheet-content button').first.click();p.wait_for_function('()=>document.getElementById("notice").textContent.includes("checksum")');self.assertEqual(p.locator('#advanced-plan').count(),0);self.close(p);p.click('#mode-seeker');self.open(p);p.locator('[data-item]').click();self.run_calc(p);self.assertIn('Practice fibre',p.locator('#calculation').inner_text())
    def test_full_backup_and_legacy_restore_preserve_advanced_drafts(self):
        p=self.page();p.on('dialog',lambda d:d.accept());self.lab(p);p.fill('#advanced-plan','unfinished draft');raw=p.evaluate('localStorage.getItem("hytale-craft-advanced-v1")');self.assertIn('unfinished draft',raw);self.close(p);p.locator('#nav [data-view=more]').click()
        with p.expect_download() as d:p.get_by_role('button',name='Export all browser data',exact=True).click()
        backup=json.loads(Path(d.value.path()).read_text());self.assertEqual(backup['advanced'],raw);legacy=dict(backup);del legacy['advanced']
        with p.expect_file_chooser() as fc:p.get_by_role('button',name='Restore all browser data',exact=True).click()
        fc.value.set_files({'name':'legacy.json','mimeType':'application/json','buffer':json.dumps(legacy).encode()});p.wait_for_function('()=>document.getElementById("notice").textContent.includes("Saved")');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-advanced-v1")'),raw)
    def test_corrupt_local_settings_are_exportable_not_overwritten(self):
        p=self.page();p.goto(self.url);p.wait_for_selector('#goals button');p.evaluate('localStorage.setItem("hytale-craft-advanced-v1","BROKEN")');self.lab(p,ready=False);p.wait_for_function('()=>document.getElementById("sheet-content").textContent.includes("damaged")');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-advanced-v1")'),'BROKEN')
    def test_offline_lab_and_missing_publication_approval(self):
        import subprocess,sys
        subprocess.run([sys.executable,'scripts/export_beta.py'],cwd=beta.ROOT,check=True,capture_output=True)
        p=self.page();requests=[];p.on('request',lambda r:requests.append(r.url));p.route('**/offline-engine.html',lambda r:r.fulfill(status=200,content_type='text/html',body=(beta.OUT/'hytale-craft-beta.html').read_text()));p.goto(self.url+'offline-engine.html');p.wait_for_selector('#goals button');p.click('#mode-maker');p.locator('[data-tool=calculator]').click();p.locator('#sheet-content button').first.click();p.wait_for_selector('#advanced-plan');self.run_calc(p);self.assertIn('Practice residue',p.locator('#advanced-result').inner_text());self.assertEqual(len(requests),1)
        p2=self.page();p2.route('**/web/build-config.js',lambda r:r.fulfill(status=200,content_type='application/javascript',body='window.CRAFT_BUILD={};'));self.lab(p2,ready=False);p2.wait_for_function('()=>document.getElementById("notice").textContent.includes("approval")');self.assertEqual(p2.locator('#advanced-plan').count(),0)

for name in list(beta.BetaTests.__dict__):
    if name.startswith('test_'):setattr(AdvancedTests,name,None)
if __name__=='__main__':unittest.main()
