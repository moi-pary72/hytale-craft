"""Mobile regression checks against a local static server; fixtures are not game data."""
import json
import os
import threading
import unittest
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright
from legacy_fixture import install

class MobileTests(unittest.TestCase):
    def test_mobile_flow(self):
        server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(Path(__file__).resolve().parents[1])))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox'])
            page=browser.new_page(reduced_motion='reduce',viewport={'width':393,'height':851},is_mobile=True,has_touch=True)
            install(page)
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m: errors.append(m.text) if m.type=='error' else None)
            page.goto(f'http://127.0.0.1:{server.server_port}/')
            page.locator('#game-source option[value=recipes]').wait_for(state='attached')
            self.assertEqual(page.locator('#target option').count(),1) # no injected samples
            page.select_option('#language','ru')
            page.locator('#goal-tiles button').first.click();page.click('#goal-go')
            page.fill('#game-search','Fixture Product')
            self.assertGreater(page.locator('#game-items button').count(),0)
            page.locator('#game-items button').first.click()
            self.assertIn('Fixture Product',page.locator('#game-card').inner_text())
            page.fill('#game-qty','2');page.fill('#game-inventory','Fixture_Rod: 1')
            page.get_by_role('button',name='Рассчитать ресурсы',exact=True).click()
            self.assertIn('5',page.locator('#game-result').inner_text())
            self.assertIn('10',page.locator('#game-result').inner_text())
            self.assertIn('Fixture_Bench',page.locator('#game-result').inner_text());page.locator('#game-card').screenshot(path='/tmp/hytale-shortbow-mobile.png')
            page.locator('#game-card').get_by_role('button',name='Сохранить инвентарь',exact=True).click()
            page.get_by_role('button',name='Добавить в план крафта',exact=True).click()
            page.click('#game-batch-run')
            self.assertIn('5',page.locator('#game-batch-result').inner_text())
            self.assertIn('10',page.locator('#game-batch-result').inner_text())
            self.assertIn('Fixture_Product: 2',page.locator('#game-goals').input_value())
            page.select_option('#language','en')
            self.assertEqual(page.locator('#game-qty').input_value(),'2')
            self.assertEqual(page.locator('#game-inventory').input_value(),'Fixture_Rod: 1')
            page.select_option('#language','ru')
            page.select_option('#game-category','all');page.fill('#game-search','Fixture_Vessel');page.locator('#game-items button[data-item-id="Fixture_Vessel"]').click()
            page.get_by_role('button',name='Рассчитать ресурсы',exact=True).click()
            self.assertIn('Recipe cycle',page.locator('#game-result').inner_text())
            # Select a direct intermediate to obtain rather than auto-craft through a conversion cycle.
            page.locator('#game-card details input[type=checkbox]').evaluate_all('(xs)=>{for(const x of xs){if(x.parentElement.textContent.includes("Clay")){x.checked=true;x.dispatchEvent(new Event("change"));}}}')
            page.get_by_role('button',name='Рассчитать ресурсы',exact=True).click()
            self.assertNotIn('Recipe cycle',page.locator('#game-result').inner_text())
            self.assertIn('Fixture_Furnace',page.locator('#game-result').inner_text())
            page.fill('#game-search','Fixture Incomplete');page.locator('#game-items button').first.click()
            self.assertIn('Полного подтверждённого рецепта нет',page.locator('#game-card').inner_text())
            self.assertEqual(page.locator('#game-qty').count(),0)
            page.get_by_role('button',name='Добавить свой рецепт',exact=True).click()
            self.assertEqual(page.locator('#name').input_value(),'Fixture_Incomplete')
            # Switching the dataset must never silently merge the older IDs with recipes.
            page.select_option('#game-source','ids');page.fill('#game-search','Fixture_Product')
            page.locator('#game-items button').first.click()
            self.assertIn('Полного подтверждённого рецепта нет',page.locator('#game-card').inner_text())
            self.assertFalse(page.evaluate('document.documentElement.scrollWidth > innerWidth'))
            page.evaluate("localStorage.setItem('hytale-craft-recipes-v1',JSON.stringify({TestTarget:{yield:2,source:'Automated test fixture',ingredients:{TestRaw:3}}}))")
            page.reload();page.locator('#goal-tiles button').first.click()
            page.click('.catalog-launch');page.click('.catalog-backdrop .catalog-result:has-text("TestTarget")')
            self.assertIn('TestRaw',page.locator('#results').inner_text())
            page.fill('#qty','3');page.locator('#inventory-more').evaluate('(e)=>e.open=true')
            page.fill('#inventory','TestRaw: 1');page.click('#save-inventory');page.click('#calc')
            self.assertIn('5',page.locator('#shopping').inner_text())
            self.assertIn('1',page.locator('#results').inner_text())
            page.reload();self.assertEqual(page.locator('#inventory').input_value(),'TestRaw: 1');page.locator('#game-source option[value=recipes]').wait_for(state='attached');self.assertIn('Fixture_Product: 2',page.locator('#game-goals').input_value())
            page.select_option('#language','en')
            self.assertIn('Game item catalog',page.locator('#game-title').inner_text())
            self.assertFalse(errors,errors)
            page.set_viewport_size({'width':320,'height':780});self.assertFalse(page.evaluate('document.documentElement.scrollWidth > innerWidth'));page.set_viewport_size({'width':393,'height':851})
            page.route('**/data/recipes/fixture.json',lambda route: route.fulfill(status=200,content_type='application/json',body='{}'))
            page.reload();page.locator('#game-items button').first.wait_for()
            page.wait_for_function("document.getElementById('game-status').textContent.includes('unavailable')")
            self.assertEqual(page.locator('#game-source option[value=recipes]').count(),0)
            self.assertFalse(page.evaluate('document.documentElement.scrollWidth > innerWidth'))
            page.screenshot(path='/tmp/hytale-mobile.png',full_page=True)
            browser.close()

if __name__=='__main__':unittest.main()
