"""Mobile regression checks against a local static server; fixtures are not game data."""
import json
import threading
import unittest
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright

class MobileTests(unittest.TestCase):
    def test_mobile_flow(self):
        server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(Path(__file__).resolve().parents[1])))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            page=browser.new_page(reduced_motion='reduce',viewport={'width':393,'height':851},is_mobile=True,has_touch=True)
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(f'http://127.0.0.1:{server.server_port}/')
            page.locator('#game-items button').first.wait_for()
            self.assertEqual(page.locator('#target option').count(),1) # no injected samples
            page.select_option('#language','ru')
            page.locator('#goal-tiles button').first.click();page.click('#goal-go')
            page.fill('#game-search','Shortbow_Crude')
            self.assertGreater(page.locator('#game-items button').count(),0)
            page.locator('#game-items button').first.click()
            self.assertIn('Подтверждённого рецепта нет',page.locator('#game-card').inner_text())
            self.assertFalse(page.evaluate('document.documentElement.scrollWidth > innerWidth'))
            page.evaluate("localStorage.setItem('hytale-craft-recipes-v1',JSON.stringify({TestTarget:{yield:2,source:'Automated test fixture',ingredients:{TestRaw:3}}}))")
            page.reload();page.locator('#goal-tiles button').first.click()
            page.click('.catalog-launch');page.click('.catalog-result:has-text("TestTarget")')
            self.assertIn('TestRaw',page.locator('#results').inner_text())
            page.fill('#qty','3');page.locator('#inventory-more').evaluate('(e)=>e.open=true')
            page.fill('#inventory','TestRaw: 1');page.click('#save-inventory');page.click('#calc')
            self.assertIn('5',page.locator('#shopping').inner_text())
            self.assertIn('1',page.locator('#results').inner_text())
            page.reload();self.assertEqual(page.locator('#inventory').input_value(),'TestRaw: 1')
            page.select_option('#language','en')
            self.assertIn('Game item catalog',page.locator('#game-title').inner_text())
            self.assertFalse(errors,errors)
            page.screenshot(path='/tmp/hytale-mobile.png',full_page=True)
            browser.close()

if __name__=='__main__':unittest.main()
