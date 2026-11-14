"""Actual user-only beta output, native dialog, history and CSP on mobile Chromium."""
import importlib.util,json,os,threading,time,unittest
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'.private/stage6';OUT.mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
    def end_headers(self):
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'none'");super().end_headers()
class BetaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        s=importlib.util.spec_from_file_location('pages',ROOT/'scripts/build_pages.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.build()
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'dist')));threading.Thread(target=cls.server.serve_forever,daemon=True).start()
        cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox']);cls.url=f'http://127.0.0.1:{cls.server.server_port}/'
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.p.stop();cls.server.shutdown();cls.server.server_close()
    def page(self,lang='en',reduced=True):
        c=self.browser.new_context(locale=lang,viewport={'width':393,'height':851},is_mobile=True,has_touch=True,reduced_motion='reduce' if reduced else 'no-preference',permissions=['clipboard-read','clipboard-write']);self.addCleanup(c.close);p=c.new_page();p.set_default_timeout(10000);return p
    def ready(self,p):p.wait_for_selector('#goals button');p.locator('.scene img').evaluate_all('(xs)=>Promise.all(xs.map(x=>x.decode()))')
    def open(self,p,goal='fight'):p.locator('[data-goal='+goal+']').click();p.wait_for_selector('#sheet[open]')
    def test_locales_widths_all_goals_no_scroll_csp(self):
        metrics=[]
        for lang in ('en','ru','es','pt-BR'):
            p=self.page(lang);errors=[];requests=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda e:errors.append(e.text) if e.type=='error' else None);p.on('request',lambda r:requests.append(r.url));p.goto(self.url);self.ready(p)
            self.assertEqual(p.locator('html').get_attribute('lang'),lang);self.assertEqual(p.locator('#goals button').count(),10);self.assertEqual(p.locator('#nav button').count(),4);self.assertFalse(any('/data/' in u or '-atlas.webp' in u for u in requests))
            for width in (320,360,393,430):
                p.set_viewport_size({'width':width,'height':851});self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'));p.screenshot(path=str(OUT/f'home-{lang}-{width}.png'),full_page=True) if lang=='ru' else None
            for goal in ('fight','defend','gather','build','survive','farm','explore','boss','skills','workshop'):
                p.locator('[data-goal='+goal+']').scroll_into_view_if_needed();y=p.evaluate('scrollY');self.open(p,goal);self.assertTrue(p.locator('#home').evaluate('(x)=>x.inert'));self.assertEqual(p.locator('#sheet-content [data-item]').count(),1);self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'));p.click('#close');p.wait_for_selector('#sheet:not([open])',state='attached');self.assertAlmostEqual(p.evaluate('scrollY'),y,delta=2)
            metrics.append({'language':lang,'startup_decoded_bytes':p.evaluate('performance.getEntriesByType("resource").reduce((n,x)=>n+x.decodedBodySize,0)'),'dataset_requests':0})
            p.select_option('#language','en' if lang!='en' else 'ru');p.reload();self.ready(p);self.assertEqual(p.locator('html').get_attribute('lang'),'en' if lang!='en' else 'ru');self.assertFalse(errors,errors)
        (OUT/'startup.json').write_text(json.dumps(metrics,indent=2))
    def test_history_focus_swipe_quantity_inventory_plan_persistence(self):
        p=self.page();p.goto(self.url);self.ready(p);self.open(p);p.locator('[data-item="lesson:blade"]').click();p.fill('#quantity','2');p.get_by_role('button',name='Calculate resources',exact=True).click();self.assertIn('6',p.locator('#calculation').inner_text());self.assertIn('Practice fibre',p.locator('#calculation').inner_text())
        p.locator('#sheet').get_by_role('button',name='My inventory',exact=True).click();p.fill('#inventory','lesson:fibre: 3');p.get_by_role('button',name='Save inventory',exact=True).click();p.go_back();p.wait_for_selector('#quantity');self.assertEqual(p.locator('#quantity').input_value(),'2');p.get_by_role('button',name='Calculate resources',exact=True).click();self.assertIn('3',p.locator('#calculation').inner_text());p.get_by_role('button',name='Add to crafting plan',exact=True).click()
        p.screenshot(path=str(OUT/'recipe-en-393.png'));p.keyboard.press('Escape');p.wait_for_selector('#sheet:not([open])',state='attached');self.assertTrue(p.evaluate('document.activeElement.matches("[data-goal=fight]")'))
        p.locator('#nav button').nth(2).click();p.wait_for_selector('#plan');self.assertIn('lesson:blade: 2',p.locator('#plan').input_value());p.get_by_role('button',name='Calculate plan',exact=True).click();self.assertIn('3',p.locator('#plan-result').inner_text());p.reload();self.ready(p);p.wait_for_selector('#plan');self.assertIn('lesson:blade: 2',p.locator('#plan').input_value());p.go_back();p.wait_for_selector('#sheet:not([open])',state='attached')
        self.open(p);p.locator('[data-item]').click();p.go_back();p.wait_for_selector('[data-item]');p.go_back();p.wait_for_selector('#sheet:not([open])',state='attached')
        self.open(p);box=p.locator('#handle').bounding_box();p.mouse.move(box['x']+box['width']/2,box['y']+10);p.mouse.down();p.mouse.move(box['x']+box['width']/2,box['y']+110,steps=8);p.mouse.up();p.wait_for_selector('#sheet:not([open])',state='attached')
    def test_loading_damage_and_isolated_user_import_export(self):
        p=self.page();p.goto(self.url);self.ready(p);p.evaluate('localStorage.setItem("hytale-craft-recipes-v1","BROKEN")');p.reload();self.ready(p);self.open(p);self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-recipes-v1")'),'BROKEN');self.assertIn('Existing data was kept',p.locator('#notice').inner_text());p.click('#close');p.wait_for_selector('#sheet:not([open])',state='attached');p.locator('#nav button').nth(3).click()
        with p.expect_download() as d:p.get_by_role('button',name='Export all browser data',exact=True).click()
        self.assertTrue(d.value.suggested_filename.endswith('.json'))
        p2=self.page();p2.route('**/web/beta/examples.js',lambda r:r.fulfill(status=200,content_type='application/javascript',body='window.CraftExamples={bad:{}};'));p2.goto(self.url);self.ready(p2);self.open(p2);self.assertIn('unavailable',p2.locator('#sheet-content').inner_text());self.assertEqual(p2.locator('[data-item]').count(),0)
    def test_animation_repeat_latency_and_slow_network(self):
        p=self.page(reduced=False);p.goto(self.url);self.ready(p)
        p.evaluate("Promise.all(['fight','gather'].map(id=>{const im=new Image();im.src='assets/art-pair/'+id+'-atlas.webp';return im.decode()}))")
        errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda e:errors.append(e.text) if e.type=='error' else None);started=time.monotonic();p.locator('[data-goal=fight]').click();p.wait_for_selector('.pose.visible');self.assertIn('fight-atlas.webp',p.locator('.pose.visible').evaluate('(x)=>getComputedStyle(x).backgroundImage'));p.wait_for_selector('#sheet[open]');elapsed=time.monotonic()-started;self.assertGreater(elapsed,.65);self.assertLess(elapsed,2);self.assertFalse(errors,errors)
        p.click('#close');p.wait_for_selector('#sheet:not([open])',state='attached');started=time.monotonic();self.open(p);self.assertLess(time.monotonic()-started,.65)
        p.screenshot(path=str(OUT/'sheet-en-393.png'))
        p2=self.page();s=p2.context.new_cdp_session(p2);s.send('Emulation.setCPUThrottlingRate',{'rate':4});s.send('Network.enable');s.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,'downloadThroughput':150000,'uploadThroughput':50000});started=time.monotonic();p2.goto(self.url);self.ready(p2);elapsed=time.monotonic()-started;self.assertLess(elapsed,15);(OUT/'slow.json').write_text(json.dumps({'cpu_slowdown':4,'latency_ms':150,'download_bytes_per_second':150000,'home_ready_seconds':round(elapsed,3)},indent=2))

    def test_user_editor_import_cycles_backup_and_keyboard(self):
        p=self.page();p.goto(self.url);self.ready(p);p.locator('#nav button').nth(3).click();p.locator('#sheet').get_by_role('button',name='My recipe editor',exact=True).click()
        p.fill('#recipe-name','Own');p.fill('#recipe-inputs','Raw: 3');p.fill('#recipe-yield','2');p.get_by_role('button',name='Save my recipe',exact=True).click();self.assertIn('Own',p.evaluate('localStorage.getItem("hytale-craft-recipes-v1")'))
        p.keyboard.press('Escape');p.wait_for_selector('#sheet:not([open])',state='attached');self.open(p);p.select_option('#scope','user');p.locator('[data-item=Own]').click();p.fill('#quantity','3');p.get_by_role('button',name='Calculate resources',exact=True).click();self.assertIn('6',p.locator('#calculation').inner_text());p.reload();self.ready(p);p.wait_for_selector('#quantity');self.assertEqual(p.locator('#quantity').input_value(),'3');self.assertIn('6',p.locator('#calculation').inner_text())
        for _ in range(15):
            p.keyboard.press('Tab');self.assertTrue(p.evaluate('document.getElementById("sheet").contains(document.activeElement)'))
        p.keyboard.press('Escape');p.wait_for_selector('#sheet:not([open])',state='attached');p.locator('#nav button').nth(3).click();p.on('dialog',lambda d:d.accept())
        recipe={'format':'hytale-craft-v1','recipes':{'Loop':{'yield':1,'source':'Synthetic browser test','ingredients':{'Loop':1}}}}
        with p.expect_file_chooser() as fc:p.get_by_role('button',name='Import my recipes',exact=True).click()
        fc.value.set_files({'name':'recipes.json','mimeType':'application/json','buffer':json.dumps(recipe).encode()});p.wait_for_function('()=>document.getElementById("notice").textContent.includes("Saved")')
        with p.expect_download() as download:p.get_by_role('button',name='Export all browser data',exact=True).click()
        data=json.loads(Path(download.value.path()).read_text());self.assertEqual(data['format'],'hytale-craft-beta-backup-v1')
        p.keyboard.press('Escape');p.wait_for_selector('#sheet:not([open])',state='attached');self.open(p);p.select_option('#scope','user');p.locator('[data-item=Loop]').click();p.get_by_role('button',name='Calculate resources',exact=True).click();self.assertIn('cycle',p.locator('#notice').inner_text())
        p.keyboard.press('Escape');p.wait_for_selector('#sheet:not([open])',state='attached');p.locator('#nav button').nth(3).click()
        with p.expect_file_chooser() as fc:p.get_by_role('button',name='Restore all browser data',exact=True).click()
        fc.value.set_files({'name':'backup.json','mimeType':'application/json','buffer':json.dumps(data).encode()});p.wait_for_function('()=>document.getElementById("notice").textContent.includes("Saved")')
        saved=p.evaluate('localStorage.getItem("hytale-craft-recipes-v1")')
        with p.expect_file_chooser() as fc:p.get_by_role('button',name='Import my recipes',exact=True).click()
        fc.value.set_files({'name':'bad.json','mimeType':'application/json','buffer':b'BROKEN'});p.wait_for_function('()=>document.getElementById("notice").textContent.includes("Invalid")');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-recipes-v1")'),saved)


    def test_offline_preview_and_missing_art(self):
        import subprocess,sys
        subprocess.run([sys.executable,'scripts/export_beta.py'],cwd=ROOT,check=True,capture_output=True)
        p=self.page();requests=[];p.on('request',lambda r:requests.append(r.url));p.route('**/offline.html',lambda r:r.fulfill(status=200,content_type='text/html',body=(OUT/'hytale-craft-beta.html').read_text()));p.goto(self.url+'offline.html');self.ready(p);self.open(p);p.locator('[data-item]').click();p.get_by_role('button',name='Calculate resources',exact=True).click();self.assertIn('Practice fibre',p.locator('#calculation').inner_text());self.assertEqual(len(requests),1)
        p2=self.page();p2.route('**/assets/**/*.webp',lambda r:r.fulfill(status=404,body=''));p2.goto(self.url);p2.wait_for_selector('#goals button');self.open(p2);self.assertTrue(p2.locator('#sheet').is_visible());self.assertEqual(p2.locator('#goals img').count(),0);self.assertEqual(p2.locator('#goals button').count(),10);self.assertEqual(p2.locator('.symbol').count(),0)

    def test_storage_failure_and_corrupt_locale(self):
        p=self.page();p.add_init_script("Storage.prototype.setItem=function(){throw new DOMException('Full','QuotaExceededError')}");p.goto(self.url);self.ready(p);p.locator('#nav button').nth(1).click();p.fill('#inventory','lesson:fibre: 2');p.get_by_role('button',name='Save inventory',exact=True).click();self.assertIn('not saved',p.locator('#notice').inner_text());self.assertIsNone(p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'))
        p2=self.page();p2.route('**/locales/beta/*.json',lambda r:r.fulfill(status=200,content_type='application/json',body='BROKEN'));p2.goto(self.url);p2.wait_for_selector('#boot-error:not([hidden])');self.assertEqual(p2.locator('#goals button').count(),0);self.assertIn('Reload',p2.locator('#boot-error').inner_text())


    def test_v2_artwork_and_navigation_inside_modal_preserve_data(self):
        p=self.page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.goto(self.url);self.ready(p)
        self.assertEqual(p.locator('#goals .scene img').count(),10)
        self.assertTrue(p.locator('#goals .scene img').evaluate_all('(xs)=>xs.every(x=>x.naturalWidth>=400)'))
        self.assertEqual(p.locator('.brand img').get_attribute('alt'),'Hytale Craft')
        self.open(p);self.assertTrue(p.locator('#sheet-nav').is_visible())
        p.locator('#sheet-nav [data-view=inventory]').click();p.fill('#inventory','lesson:fibre: 7');p.get_by_role('button',name='Save inventory',exact=True).click()
        saved=p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")')
        p.locator('#sheet-nav [data-view=plan]').click();p.wait_for_selector('#plan');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'),saved)
        p.locator('#sheet-nav [data-view=home]').click();p.wait_for_selector('#sheet:not([open])',state='attached');self.assertTrue(p.locator('#nav').is_visible())
        p.reload();self.ready(p);self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-inventory-v1")'),saved);self.assertFalse(errors,errors)

    def test_language_preference_survives_reload_during_pending_fetch(self):
        p=self.page();session=p.context.new_cdp_session(p);session.send('Network.enable');session.send('Network.setCacheDisabled',{'cacheDisabled':True});session.send('Network.emulateNetworkConditions',{'offline':False,'latency':250,'downloadThroughput':1000000,'uploadThroughput':1000000})
        p.goto(self.url);self.ready(p);p.select_option('#language','ru');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-language")'),'ru');p.reload();self.ready(p);self.assertEqual(p.locator('html').get_attribute('lang'),'ru');self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-language")'),'ru')

if __name__=='__main__':unittest.main()
