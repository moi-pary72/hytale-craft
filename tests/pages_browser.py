"""Validate the actual allowlisted Pages output without deploying it."""
import importlib.util
import json
import os
import threading
import unittest
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
    def end_headers(self):
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'none'")
        super().end_headers()
class PagesBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('pages',ROOT/'scripts/build_pages.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.build()
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'dist')))
        threading.Thread(target=cls.server.serve_forever,daemon=True).start()
        cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox'])
        cls.url=f'http://127.0.0.1:{cls.server.server_port}/'
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.p.stop();cls.server.shutdown();cls.server.server_close()
    def test_user_only_build_four_locales_mobile_csp_and_persistence(self):
        for lang in ('en','ru','es','pt-BR'):
            context=self.browser.new_context(locale=lang,viewport={'width':393,'height':851},is_mobile=True,has_touch=True)
            try:
                p=context.new_page();errors=[];requests=[]
                p.on('pageerror',lambda e:errors.append(str(e)))
                p.on('console',lambda e:errors.append(e.text) if e.type=='error' else None)
                p.on('request',lambda r:requests.append(r.url));p.goto(self.url)
                p.wait_for_selector('#goals button');self.assertEqual(p.locator('html').get_attribute('lang'),lang)
                for goal in ('fight','defend','gather','build','survive','farm','explore','boss','skills','workshop'):
                    p.locator('[data-goal='+goal+']').click();self.assertEqual(p.locator('#source').input_value(),'user')
                self.assertFalse(any('/data/' in u for u in requests))
                self.assertEqual(p.locator('#source option:disabled').count(),2)
                p.locator('#tools').evaluate('(x)=>x.open=true');p.locator('#editor-panel').evaluate('(x)=>x.open=true')
                p.fill('#recipe-name','Synthetic fixture');p.fill('#recipe-inputs','Raw: 3');p.fill('#recipe-yield','2');p.locator('#editor button[type=submit]').click()
                p.reload();p.wait_for_selector('#goals button');p.locator('[data-goal=fight]').click();p.locator('[data-item="Synthetic fixture"]').click();p.fill('#quantity','3')
                d=json.loads((ROOT/'locales'/f'{lang}.json').read_text());p.locator('#item-card button').filter(has_text=d['calculate']).click();self.assertIn('6',p.locator('#card-result').inner_text())
                for w in (320,360,393,430):
                    p.set_viewport_size({'width':w,'height':851});self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'))
                self.assertFalse(errors,errors)
            finally:context.close()
    def test_unknown_route_is_404_not_legacy_or_spa(self):
        context=self.browser.new_context();p=context.new_page()
        try:
            self.assertEqual(p.goto(self.url+'missing').status,404)
            self.assertEqual(p.request.get(self.url+'docs/PROJECT_STATE.md').status,404)
            self.assertEqual(p.request.get(self.url+'data/catalog.json').status,404)
        finally:context.close()
if __name__=='__main__':unittest.main()
