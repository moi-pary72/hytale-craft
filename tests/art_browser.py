"""Two-card reference-led art review: no data publication, no live deployment."""
import json,os,threading,time,unittest
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.private/stage5';OUT.mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
class ArtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));threading.Thread(target=cls.server.serve_forever,daemon=True).start()
        cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox']);cls.url=f'http://127.0.0.1:{cls.server.server_port}/art-preview.html'
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.p.stop();cls.server.shutdown();cls.server.server_close()
    def page(self,lang='en',motion='no-preference',video=False):
        c=self.browser.new_context(viewport={'width':393,'height':851},locale=lang,is_mobile=True,has_touch=True,reduced_motion=motion,**({'record_video_dir':str(OUT/'video'),'record_video_size':{'width':393,'height':851}} if video else {}));self.addCleanup(c.close);p=c.new_page();p.set_default_timeout(10000);return p
    def ready(self,p):p.wait_for_selector('#goals.art-pair button[data-goal=gather]');p.locator('#goals img').evaluate_all('(imgs)=>Promise.all(imgs.map(x=>x.decode()))')
    def test_four_locales_widths_assets_and_keyboard(self):
        metrics=[]
        for lang in ('en','ru','es','pt-BR'):
            p=self.page(lang);errors=[];requests=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda e:errors.append(e.text) if e.type=='error' else None);p.on('request',lambda r:requests.append(r.url));p.goto(self.url);self.ready(p)
            self.assertEqual(p.locator('html').get_attribute('lang'),lang);self.assertEqual(p.locator('#goals button').count(),2);self.assertEqual(p.locator('#art-pending button').count(),8)
            self.assertFalse(any('/data/' in x or '-atlas.webp' in x or '/assets/preview/' in x for x in requests),requests)
            for w in (320,360,393,430):
                p.set_viewport_size({'width':w,'height':851});self.assertEqual(p.locator('#goals').evaluate('(x)=>getComputedStyle(x).gridTemplateColumns.split(" ").length'),2);self.assertFalse(p.evaluate('document.documentElement.scrollWidth>innerWidth'))
                if lang in ('en','ru'):p.screenshot(path=str(OUT/f'art-{lang}-{w}.png'),full_page=True)
            p.keyboard.press('Tab');self.assertTrue(p.locator('.skip').evaluate('(x)=>x===document.activeElement'))
            metrics.append({'locale':lang,'startup_decoded_bytes':p.evaluate('performance.getEntriesByType("resource").reduce((n,x)=>n+x.decodedBodySize,0)'),'requests':len(requests),'data_requests':0,'atlas_before_interaction':0})
            self.assertFalse(errors,errors)
        (OUT/'startup.json').write_text(json.dumps(metrics,indent=2))
    def test_one_shot_real_pose_changes_cancel_and_navigation(self):
        p=self.page(video=True);p.goto(self.url);self.ready(p)
        p.locator('[data-replay=fight]').click();p.wait_for_selector('[data-goal=fight][data-playing=true]')
        p.wait_for_function('document.querySelector("[data-goal=fight] .art-sprite").dataset.frame==="1"')
        p.screenshot(path=str(OUT/'fight-action.png'))
        p.locator('[data-replay=gather]').click();p.wait_for_selector('[data-goal=gather][data-playing=true]');self.assertEqual(p.locator('[data-playing=true]').count(),1)
        p.wait_for_function('document.querySelector("[data-goal=gather] .art-sprite").dataset.frame==="2"');p.screenshot(path=str(OUT/'gather-impact.png'))
        p.wait_for_function('document.querySelectorAll("[data-playing=true]").length===0');self.assertEqual(p.evaluate('document.getAnimations().length'),0)
        p.locator('[data-goal=fight]').focus();p.wait_for_selector('[data-playing=true]');p.locator('#art-motion').uncheck();self.assertEqual(p.locator('[data-playing=true]').count(),0)
        p.locator('[data-goal=fight]').tap();self.assertTrue(p.locator('#browser').is_visible());self.assertEqual(p.locator('#source').input_value(),'user')
        p.locator('#art-pending').evaluate('(x)=>x.open=true');p.locator('[data-goal=workshop]').click();self.assertTrue(p.locator('#browser').is_visible())
        p.context.close()
    def test_motion_disabled_failure_and_user_storage(self):
        p=self.page(motion='reduce');requests=[];p.on('request',lambda r:requests.append(r.url));p.goto(self.url);self.ready(p);p.locator('[data-replay=fight]').click();self.assertEqual(p.locator('[data-playing=true]').count(),0);self.assertFalse(any('-atlas.webp' in x for x in requests));self.assertTrue(p.locator('#art-motion').is_disabled())
        p.locator('[data-goal=fight]').click();p.locator('#tools').evaluate('(x)=>x.open=true');p.locator('#editor-panel').evaluate('(x)=>x.open=true');p.fill('#recipe-name','Art fixture');p.fill('#recipe-inputs','Raw: 3');p.locator('#editor button[type=submit]').click();p.reload();self.ready(p);p.locator('[data-goal=fight]').click();p.locator('[data-item="Art fixture"]').click();p.locator('#item-card button').filter(has_text='Calculate resources').click();self.assertIn('3',p.locator('#card-result').inner_text())
        p2=self.page();p2.route('**/*-atlas.webp',lambda r:r.fulfill(status=404,body=''));p2.goto(self.url);self.ready(p2);p2.locator('[data-replay=fight]').click();p2.wait_for_function('document.querySelector("#art-status").textContent.includes("unavailable")');self.assertEqual(p2.locator('[data-playing=true]').count(),0);self.assertTrue(p2.locator('#goals img').first.evaluate('(x)=>x.naturalWidth>0'))
        p3=self.page();p3.add_init_script("Object.defineProperty(navigator,'connection',{value:Object.assign(new EventTarget(),{saveData:true})})");p3.goto(self.url);self.ready(p3);p3.locator('[data-replay=gather]').click();self.assertTrue(p3.locator('#art-motion').is_disabled());self.assertEqual(p3.locator('[data-playing=true]').count(),0)
    def test_slow_network_and_offline_html(self):
        p=self.page();s=p.context.new_cdp_session(p);s.send('Emulation.setCPUThrottlingRate',{'rate':4});s.send('Network.enable');s.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,'downloadThroughput':150000,'uploadThroughput':50000});started=time.monotonic();p.goto(self.url);self.ready(p);elapsed=time.monotonic()-started;self.assertLess(elapsed,15)
        (OUT/'slow.json').write_text(json.dumps({'cpu_slowdown':4,'latency_ms':150,'download_bytes_per_second':150000,'two_posters_decoded_seconds':round(elapsed,3)},indent=2))
        import subprocess,sys
        subprocess.run([sys.executable,'scripts/build_art_preview.py','--offline'],cwd=ROOT,check=True,capture_output=True)
        p2=self.page();requests=[];p2.on('request',lambda r:requests.append(r.url));p2.route('**/art-offline.html',lambda r:r.fulfill(status=200,content_type='text/html',body=(OUT/'art-pair-mobile.html').read_text()));p2.goto(self.url.replace('art-preview.html','art-offline.html'));self.ready(p2);p2.locator('[data-replay=gather]').click();p2.wait_for_selector('[data-playing=true]');self.assertEqual(len(requests),1)
if __name__=='__main__':unittest.main()
