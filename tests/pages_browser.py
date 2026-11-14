"""Deployment boundary checks; beta_browser.py covers interactive behavior."""
import importlib.util,os,threading,unittest
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
class PagesBoundaryTests(unittest.TestCase):
    def test_actual_output_and_routes(self):
        s=importlib.util.spec_from_file_location('pages',ROOT/'scripts/build_pages.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);out=m.build()
        server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(out)));threading.Thread(target=server.serve_forever,daemon=True).start()
        try:
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox']);page=browser.new_page();base=f'http://127.0.0.1:{server.server_port}/'
                self.assertEqual(page.goto(base).status,200);page.wait_for_selector('#goals button');self.assertEqual(page.locator('#goals button').count(),10)
                for path in ('missing','docs/PROJECT_STATE.md','data/catalog.json','data/recipes/manifest.json','tests/beta_browser.py','.git/config','art-preview.html'):
                    self.assertEqual(page.request.get(base+path).status,404)
                self.assertIn('noindex',page.locator('meta[name=robots]').get_attribute('content'));self.assertIn('noindex',(out/'_headers').read_text());browser.close()
        finally:server.shutdown();server.server_close()
if __name__=='__main__':unittest.main()
