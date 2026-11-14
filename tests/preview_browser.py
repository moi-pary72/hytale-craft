"""International design preview integration. Original game data remain unchanged."""
import json
import os
import threading
import unittest
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

class PreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
        threading.Thread(target=cls.server.serve_forever,daemon=True).start()
        cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox'])
        cls.url=f'http://127.0.0.1:{cls.server.server_port}/preview.html'
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.p.stop();cls.server.shutdown();cls.server.server_close()
    def page(self,locale='en-US',width=393):
        c=self.browser.new_context(locale=locale,viewport={'width':width,'height':851},is_mobile=True,has_touch=True,reduced_motion='reduce',permissions=['clipboard-read','clipboard-write'])
        self.addCleanup(c.close);p=c.new_page();p.set_default_timeout(10000);return p
    def ready(self,p):
        p.wait_for_function('document.querySelector("#goals button")!==null')
    def test_international_home_and_mobile_budget(self):
        metrics=[]
        for lang,native in [('en','en-US'),('ru','ru-RU'),('es','es-MX'),('pt-BR','pt-BR')]:
            p=self.page(native);errors=[];requests=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:requests.append(r.url));p.goto(self.url);self.ready(p)
            self.assertEqual(p.locator('html').get_attribute('lang'),lang)
            self.assertEqual(p.locator('#goals button').count(),10)
            self.assertEqual(p.locator('#goals').evaluate('(x)=>getComputedStyle(x).gridTemplateColumns.split(" ").length'),2)
            self.assertFalse(any('/data/' in url for url in requests))
            self.assertEqual(p.locator('video,audio,iframe').count(),0)
            self.assertEqual(p.evaluate('document.getAnimations().length'),0)
            for width in (320,360,393,430):
                p.set_viewport_size({'width':width,'height':851});self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'))
            p.keyboard.press('Tab');self.assertTrue(p.locator('.skip').evaluate('(x)=>x===document.activeElement'))
            p.keyboard.press('Enter');p.keyboard.press('Tab');self.assertTrue(p.evaluate('document.activeElement.matches("button")'))
            entries=p.evaluate('performance.getEntriesByType("resource").map(x=>({url:x.name,bytes:x.decodedBodySize}))')
            startup=sum(e['bytes'] for e in entries);self.assertLess(startup,200000)
            metrics.append({'language':lang,'startup_decoded_bytes':startup,'requests':len(requests),'data_requests_before_goal':0,'widths':[320,360,393,430]})
            p.select_option('#language','en' if lang!='en' else 'ru');p.reload();self.ready(p);self.assertEqual(p.locator('html').get_attribute('lang'),'en' if lang!='en' else 'ru')
            self.assertFalse(errors,errors)
            if lang=='en':
                for w in (320,360,393,430):
                    p.set_viewport_size({'width':w,'height':851});p.screenshot(path=f'/tmp/hytale-stage4-{w}.png',full_page=True)
        Path('/tmp/hytale-preview-performance.json').write_text(json.dumps(metrics,indent=2))
    def test_all_languages_real_recipe_and_user_data(self):
        p=self.page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.goto(self.url);self.ready(p)
        original={'Fixture':{'yield':2,'source':'Synthetic test fixture','ingredients':{'Raw':3}}}
        p.evaluate('(d)=>localStorage.setItem("hytale-craft-recipes-v1",JSON.stringify(d))',original);p.reload();self.ready(p)
        p.locator('[data-goal=fight]').click();p.locator('#items [data-item="Weapon_Shortbow_Crude"]').click()
        for lang in ('en','ru','es','pt-BR'):
            p.select_option('#language',lang);p.wait_for_function('(l)=>document.documentElement.lang===l',arg=lang)
            d=json.loads((ROOT/'locales'/f'{lang}.json').read_text())
            self.assertIn(d['credit'],p.locator('#item-card').inner_text())
            p.fill('#quantity','2');p.locator('#item-card button').filter(has_text=d['calculate']).click()
            self.assertIn('Stick',p.locator('#card-result').inner_text());self.assertIn('12',p.locator('#card-result').inner_text())
            self.assertNotIn('Расчёт',p.locator('#item-card').inner_text()) if lang not in ('ru',) else None
        p.select_option('#language','en');p.wait_for_function('document.documentElement.lang==="en"')
        p.locator('#item-card button').filter(has_text='My inventory').click();p.fill('#inventory','Ingredient_Stick: 3');p.click('#save-inventory');p.locator('#item-card button').filter(has_text='Calculate resources').click();self.assertIn('5',p.locator('#card-result').inner_text())
        p.locator('#card-result button').click();self.assertIn('Ingredient_Stick',p.evaluate('navigator.clipboard.readText()'))
        p.locator('#item-card button').filter(has_text='Add to crafting plan').click();p.click('#run-plan');self.assertIn('5',p.locator('#plan-result').inner_text())
        p.reload();self.ready(p);self.assertEqual(p.locator('#inventory').input_value(),'Ingredient_Stick: 3');self.assertEqual(p.evaluate('JSON.parse(localStorage.getItem("hytale-craft-recipes-v1"))'),original)
        p.locator('[data-goal=fight]').click();p.select_option('#source','user');p.locator('#items [data-item="Fixture"]').click();p.fill('#quantity','3');p.locator('#item-card button').filter(has_text='Calculate resources').click();self.assertIn('6',p.locator('#card-result').inner_text())
        p.locator('#editor-panel').evaluate('(x)=>x.open=true');p.locator('#tools').evaluate('(x)=>x.open=true');p.fill('#recipe-name','CreatedInPreview');p.fill('#recipe-inputs','Raw: 2');p.locator('#editor button[type=submit]').click();self.assertIn('CreatedInPreview',p.evaluate('JSON.parse(localStorage.getItem("hytale-craft-recipes-v1"))'))
        with p.expect_download() as saved:p.click('#export')
        self.assertTrue(saved.value.suggested_filename.endswith('.json'))
        p.on('dialog',lambda dialog:dialog.accept());p.set_input_files('#file',{'name':'invalid.json','mimeType':'application/json','buffer':b'{}'});p.wait_for_function('document.getElementById("notice").textContent.includes("Invalid recipe backup")');self.assertIn('CreatedInPreview',p.evaluate('JSON.parse(localStorage.getItem("hytale-craft-recipes-v1"))'))
        self.assertFalse(errors,errors)
    def test_plan_can_start_before_catalog_load_and_corrupt_user_data_is_preserved(self):
        p=self.page();p.goto(self.url);self.ready(p);p.locator('#tools').evaluate('(x)=>x.open=true');p.locator('#plan-panel').evaluate('(x)=>x.open=true');p.fill('#plan','Weapon_Shortbow_Crude: 2');p.click('#run-plan');p.wait_for_function('document.getElementById("plan-result").textContent.includes("12")')
        self.assertIn('Weapon_Shortbow_Crude: 2',p.locator('#plan').input_value())
        p.evaluate('localStorage.setItem("hytale-craft-recipes-v1","BROKEN")');p.reload();self.ready(p);self.assertEqual(p.evaluate('localStorage.getItem("hytale-craft-recipes-v1")'),'BROKEN');self.assertIn('Existing data was kept',p.locator('#notice').inner_text())

    def test_self_contained_export_without_subresource_requests(self):
        import subprocess,sys,tempfile
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'offline.html'
            subprocess.run([sys.executable,'scripts/export_preview.py','--output',str(output)],cwd=ROOT,check=True,capture_output=True)
            p=self.page();requests=[];errors=[];p.on('request',lambda r:requests.append(r.url));p.on('pageerror',lambda e:errors.append(str(e)))
            p.route('**/offline.html',lambda route:route.fulfill(status=200,content_type='text/html',body=output.read_text()))
            p.goto(self.url.replace('preview.html','offline.html'));self.ready(p);p.locator('[data-goal=fight]').click();p.locator('[data-item="Weapon_Shortbow_Crude"]').click();p.fill('#quantity','2');p.locator('#item-card button').filter(has_text='Calculate resources').click()
            self.assertIn('12',p.locator('#card-result').inner_text());self.assertEqual(len(requests),1);self.assertFalse(errors,errors)

    def test_slow_phone_startup_and_reduced_motion(self):
        import time
        p=self.page();session=p.context.new_cdp_session(p);session.send('Emulation.setCPUThrottlingRate',{'rate':4});session.send('Network.enable');session.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,'downloadThroughput':150000,'uploadThroughput':50000})
        started=time.monotonic();p.goto(self.url);self.ready(p);p.locator('#goals img').first.evaluate('(x)=>x.decode()');elapsed=time.monotonic()-started
        self.assertLess(elapsed,15);self.assertEqual(p.evaluate('document.getAnimations().length'),0)
        self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'))
        p.screenshot(path='/tmp/hytale-preview-en.png',full_page=True)
        Path('/tmp/hytale-preview-slow-phone.json').write_text(json.dumps({'cpu_slowdown':4,'latency_ms':150,'download_bytes_per_second':150000,'home_ready_seconds':round(elapsed,3),'continuous_animations':0},indent=2))

    def test_corrupt_snapshot_and_missing_data(self):
        for bad in ('corrupt','missing'):
            p=self.page();p.route('**/data/recipes/*.json',lambda route:route.fulfill(status=200,content_type='application/json',body='{}'))
            if bad=='missing':p.route('**/data/catalog.json',lambda route:route.fulfill(status=200,content_type='application/json',body='{}'))
            p.goto(self.url);self.ready(p);p.locator('[data-goal=fight]').click()
            p.wait_for_function('document.getElementById("source").value!=="recipes"')
            self.assertEqual(p.locator('#source').input_value(),'ids' if bad=='corrupt' else 'user')
            self.assertEqual(p.locator('#quantity').count(),0)
            self.assertTrue(p.locator('#retry').is_visible())
            self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'))


    def test_all_goals_clear_previous_card_and_external_editor_changes(self):
        p=self.page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        p.goto(self.url);self.ready(p)
        p.locator('[data-goal=fight]').click();p.locator('[data-item="Weapon_Shortbow_Crude"]').click()
        self.assertTrue(p.locator('#item-card').is_visible())
        for goal in ('defend','gather','build','survive','farm','explore','boss','skills','workshop','fight'):
            p.locator('[data-goal='+goal+']').click()
            self.assertFalse(p.locator('#item-card').is_visible())
            self.assertTrue(p.locator('#browser').is_visible())
            self.assertEqual(p.locator('[aria-pressed=true]').count(),1)
        p.locator('#tools').evaluate('(x)=>x.open=true');p.locator('#editor-panel').evaluate('(x)=>x.open=true')
        p.fill('#recipe-name','Unsaved');p.fill('#recipe-inputs','Raw: 1')
        other={'OtherTab':{'yield':1,'source':'Synthetic fixture','ingredients':{'Raw':2}}}
        p.evaluate('(d)=>localStorage.setItem("hytale-craft-recipes-v1",JSON.stringify(d))',other)
        p.locator('#editor button[type=submit]').click()
        self.assertEqual(p.evaluate('JSON.parse(localStorage.getItem("hytale-craft-recipes-v1"))'),other)
        self.assertIn('another tab',p.locator('#notice').inner_text())
        self.assertFalse(errors,errors)

    def test_malformed_metadata_falls_back_without_javascript_crash(self):
        p=self.page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
        p.route('**/data/recipes/*.json',lambda r:r.fulfill(status=200,body='{}',content_type='application/json'))
        p.route('**/data/catalog.json',lambda r:r.fulfill(status=200,body='{"schema_version":1,"items":[{"id":"X","category":"tools"}],"source_generated_at":42}',content_type='application/json'))
        p.goto(self.url);self.ready(p);p.locator('[data-goal=gather]').click()
        p.wait_for_function('document.querySelector("#source").value==="user"')
        self.assertTrue(p.locator('#retry').is_visible());self.assertFalse(errors,errors)


    def test_slow_json_load_and_timeout_then_retry(self):
        p=self.page();p.set_default_timeout(20000)
        session=p.context.new_cdp_session(p);session.send('Network.enable');session.send('Network.emulateNetworkConditions',{'offline':False,'latency':200,'downloadThroughput':400000,'uploadThroughput':50000})
        p.goto(self.url);self.ready(p);p.locator('[data-goal=fight]').click();p.locator('[data-item="Weapon_Shortbow_Crude"]').click()
        self.assertTrue(p.locator('#quantity').is_visible())
        p2=self.page();p2.add_init_script('''window.CRAFT_BUILD={requestTimeoutMs:500};const realFetch=window.fetch.bind(window);window.blockTestData=true;window.fetch=(url,options)=>window.blockTestData&&String(url).startsWith('data/')?new Promise((resolve,reject)=>options.signal.addEventListener('abort',()=>reject(new DOMException('Timeout fixture','AbortError')))):realFetch(url,options);''')
        p2.goto(self.url);self.ready(p2);p2.locator('[data-goal=fight]').click()
        p2.wait_for_function('document.getElementById("source").value==="user"')
        self.assertTrue(p2.locator('#retry').is_visible())
        p2.evaluate('window.blockTestData=false');p2.click('#retry')
        p2.wait_for_function('document.querySelector("#source option[value=recipes]").disabled===false')
        p2.select_option('#source','recipes');p2.locator('[data-item="Weapon_Shortbow_Crude"]').click()
        self.assertTrue(p2.locator('#quantity').is_visible())

if __name__=='__main__':unittest.main()
