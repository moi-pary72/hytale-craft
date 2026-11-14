"""Verify audited dist at the GitHub project subpath, with its HTML CSP."""
import importlib.util,os,shutil,tempfile,threading,unittest
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
class ProjectPathTests(unittest.TestCase):
    def test_project_path_mobile_and_meta_csp(self):
        s=importlib.util.spec_from_file_location('pages',ROOT/'scripts/build_pages.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);out=m.build(base_path='/hytale-craft/')
        with tempfile.TemporaryDirectory(dir=ROOT/'.private') as tmp:
            shutil.copytree(out,Path(tmp)/'hytale-craft');server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=tmp));threading.Thread(target=server.serve_forever,daemon=True).start()
            try:
                with sync_playwright() as p:
                    b=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox']);page=b.new_page(viewport={'width':393,'height':851},is_mobile=True,has_touch=True,reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda e:errors.append(e.text) if e.type=='error' else None)
                    base=f'http://127.0.0.1:{server.server_port}/hytale-craft/';page.goto(base);page.wait_for_selector('#goals button');self.assertEqual(page.locator('#goals button').count(),10)
                    for width in (320,360,393,430):page.set_viewport_size({'width':width,'height':851});self.assertFalse(page.evaluate('document.documentElement.scrollWidth>innerWidth'))
                    page.locator('[data-goal=fight]').click();page.locator('[data-item="lesson:blade"]').click();page.fill('#quantity','2');page.get_by_role('button',name='Calculate resources',exact=True).click();self.assertIn('6',page.locator('#calculation').inner_text());page.go_back();page.wait_for_selector('[data-item]');page.go_back();page.wait_for_selector('#sheet:not([open])',state='attached');self.assertFalse(errors,errors)
                    self.assertEqual(page.request.get(base+'data/recipes/manifest.json').status,404);b.close()
            finally:server.shutdown();server.server_close()
if __name__=='__main__':unittest.main()
