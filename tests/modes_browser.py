"""Seeker/Maker integration against the exact public build; isolated browser storage."""
import json,unittest
from pathlib import Path
import beta_browser as beta
OUT=beta.OUT

class ModesTests(beta.BetaTests):
    # Reuse server helpers, not the inherited beta test cases.
    def maker(self,p):
        p.goto(self.url);p.wait_for_selector('#mode-maker');p.click('#mode-maker');p.wait_for_selector('#maker-tools button')
    def tool(self,p,key):p.locator('[data-tool='+key+']').click();p.wait_for_selector('#sheet[open]')
    def close(self,p):p.keyboard.press('Escape');p.wait_for_selector('#sheet:not([open])',state='attached')
    def test_modes_locales_widths_tools_and_persistence(self):
        for lang in ('en','ru','es','pt-BR'):
            p=self.page(lang);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));self.maker(p)
            self.assertEqual(p.locator('#maker-tools button').count(),8)
            for width in (320,360,393,430):
                p.set_viewport_size({'width':width,'height':851});self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'))
                p.screenshot(path=str(OUT/f'maker-{lang}-{width}.png'),full_page=True)
            for key in ('calculator','inventory','projects','tree','resources','stations','editor','transfer'):
                self.tool(p,key);self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'));self.assertTrue(p.locator('#home').evaluate('(e)=>e.inert'));self.close(p)
            p.reload();p.wait_for_selector('#maker-tools button');self.assertEqual(p.locator('#mode-maker').get_attribute('aria-pressed'),'true')
            p.click('#mode-seeker');p.wait_for_selector('#goals button');self.assertEqual(p.locator('#goals button').count(),10);self.assertFalse(errors,errors)
    def test_shared_inventory_project_tree_and_back(self):
        p=self.page();self.maker(p);self.tool(p,'inventory');p.fill('#inventory','lesson:fibre: 3');p.get_by_role('button',name='Save inventory',exact=True).click();self.close(p)
        self.tool(p,'calculator');p.locator('[data-item="lesson:blade"]').click();p.fill('#quantity','2');p.get_by_role('button',name='Add to crafting plan',exact=True).click();p.go_back();p.wait_for_selector('#filter');self.close(p)
        p.locator('#nav [data-view=plan]').click();p.get_by_role('button',name='Save as project',exact=True).click();p.fill('#project-name','My expedition');p.locator('#project-save button').click();self.assertEqual(len(json.loads(p.evaluate('localStorage.getItem("hytale-craft-projects-v1")'))),1);self.close(p)
        self.tool(p,'projects');p.locator('[data-project] button').first.click();p.wait_for_selector('#plan');p.get_by_role('button',name='Calculate plan',exact=True).click();self.assertIn('3',p.locator('#plan-result').inner_text());self.close(p)
        self.tool(p,'tree');p.select_option('#tool-item','lesson:blade');self.assertIn('Practice fibre',p.locator('#tool-result').inner_text());self.assertGreater(p.locator('.tree-node').count(),2);self.close(p)
        self.tool(p,'resources');self.assertIn('Practice fibre',p.locator('#tool-result').inner_text());self.close(p)
        p.click('#mode-seeker');self.open(p);p.locator('[data-item]').click();p.fill('#quantity','2');p.get_by_role('button',name='Calculate resources',exact=True).click();self.assertIn('3',p.locator('#calculation').inner_text());self.close(p);p.reload();self.ready(p);self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'),'lesson:fibre: 3')
    def test_stations_backup_and_corrupt_projects_preserved(self):
        p=self.page();self.maker(p);self.tool(p,'editor');p.fill('#recipe-name','My part');p.fill('#recipe-inputs','Raw: 2');p.fill('#recipe-stations','My forge');p.get_by_role('button',name='Save my recipe',exact=True).click();self.close(p)
        self.tool(p,'stations');self.assertIn('My forge',p.locator('#sheet-content').inner_text());p.locator('[data-item]').click();self.assertIn('My forge',p.locator('#sheet-content').inner_text());self.close(p)
        p.evaluate('localStorage.setItem("hytale-craft-projects-v1","BROKEN")');self.tool(p,'projects');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-projects-v1")'),'BROKEN');self.assertEqual(p.locator('[data-project]').count(),0);self.close(p)
        self.tool(p,'transfer')
        with p.expect_download() as d:p.get_by_role('button',name='Export all browser data',exact=True).click()
        backup=json.loads(Path(d.value.path()).read_text());self.assertEqual(backup['projects'],'BROKEN');self.assertIn('My part',backup['recipes']);self.assertIn('My forge',backup['recipes'])

    def test_backup_roundtrip_legacy_restore_and_rejection(self):
        p=self.page();self.maker(p);p.on('dialog',lambda d:d.accept())
        projects=[{'id':'original','name':'My plan','scope':'demo','plan':'lesson:blade: 2','updatedAt':'2026-11-15T00:00:00Z'}]
        raw=json.dumps(projects);p.evaluate('(v)=>localStorage.setItem("hytale-craft-projects-v1",v)',raw);self.tool(p,'transfer')
        with p.expect_download() as d:p.get_by_role('button',name='Export all browser data',exact=True).click()
        backup=json.loads(Path(d.value.path()).read_text());self.assertEqual(backup['projects'],raw)
        def restore(data):
            with p.expect_file_chooser() as fc:p.get_by_role('button',name='Restore all browser data',exact=True).click()
            fc.value.set_files({'name':'backup.json','mimeType':'application/json','buffer':json.dumps(data).encode()})
        p.evaluate('localStorage.setItem("hytale-craft-projects-v1","[]")');restore(backup);p.wait_for_function('()=>document.getElementById("notice").textContent.includes("Saved")');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-projects-v1")'),raw)
        legacy=dict(backup);del legacy['projects'];restore(legacy);p.wait_for_function('()=>document.getElementById("notice").textContent.includes("Saved")');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-projects-v1")'),raw)
        invalid=dict(backup);invalid['projects']='BROKEN';invalid['inventory']='Raw: 99';restore(invalid);p.wait_for_function('()=>document.getElementById("notice").textContent.includes("Invalid")');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-projects-v1")'),raw);self.assertNotEqual(p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'),'Raw: 99')

# Inherited cases are run separately by beta_browser.py.
for name in list(beta.BetaTests.__dict__):
    if name.startswith('test_'):setattr(ModesTests,name,None)
if __name__=='__main__':unittest.main()
