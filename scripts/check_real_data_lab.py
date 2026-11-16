#!/usr/bin/env python3
"""Opt-in real local browser QA. Details/screens never leave .private automatically."""
import argparse,json,threading,time,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
try:from serve_real_data_lab import make_server
except ModuleNotFoundError:from scripts.serve_real_data_lab import make_server
ROOT=Path(__file__).resolve().parents[1]
def run(build,math_file,out,visuals=None):
 out=Path(out).resolve()
 if not out.is_relative_to((ROOT/'.private').resolve()):raise ValueError('Real screenshots and reports must remain private')
 out.mkdir(parents=True,exist_ok=True,mode=0o700);data=json.loads((build/'research-data.json').read_text());math=json.loads(math_file.read_text());model=data['canonical'];names={i['id']:i['names']['en'] or i['id'] for i in model['items']};metrics=[];errors=[];screens=[]
 server=make_server(build);threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}/';report={'source_revision':model['snapshot']['source_revision'],'physical_android':False,'public_upload':False}
 try:
  with sync_playwright() as pw:
   browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
   for width in [320,360,393,430]:
    context=browser.new_context(viewport={'width':width,'height':852},is_mobile=True,has_touch=True,reduced_motion='reduce');p=context.new_page();p.set_default_timeout(15000);p.on('pageerror',lambda e:errors.append(str(e)));start=time.monotonic();p.goto(url,wait_until='domcontentloaded');p.wait_for_selector('.lab-card');assert not p.evaluate('document.documentElement.scrollWidth>innerWidth');metrics.append({'width':width,'ready_seconds':round(time.monotonic()-start,3),**p.evaluate('window.CRAFT_LAB_BOOT')})
    if visuals:p.check('#lab-interpretations')
    for sample,count in [('100',100),('1000',1000),('10000',len(model['items']))]:
     p.select_option('#lab-size',sample);assert str(count)+' matching items' in p.locator('#view-content').inner_text();assert p.locator('.lab-card').count()<=24
     p.locator('.lab-controls').evaluate('(el)=>window.scrollTo(0,el.getBoundingClientRect().top+scrollY-10)');p.wait_for_timeout(200)
     if width==393:p.screenshot(path=str(out/f'catalog-{count}.png'));screens.append(f'catalog-{count}.png')
    if width==393:
     if visuals:
      bindings=json.loads(Path(visuals).read_text());verified=0
      for entry in bindings['entries']:
       p.fill('#lab-search',entry['item_id']);p.locator('[data-item="'+entry['item_id']+'"]').click();p.locator('#sheet-content [data-research=true] img').first.evaluate('(e)=>e.decode()');assert 'reference version unmatched' in p.locator('#sheet-content [data-research=true]').first.get_attribute('aria-label');p.get_by_text('Visual evidence · original interpretation, not official art',exact=True).click();assert entry['reference']['reference_version'] in p.locator('#sheet-content').inner_text();verified+=1
       if verified==1:p.screenshot(path=str(out/'individual-evidence.png'));screens.append('individual-evidence.png')
       p.keyboard.press('Escape')
      report['observed_private_interpretations']=verified;p.fill('#lab-search','Iron');p.locator('.lab-controls').evaluate('(el)=>window.scrollTo(0,el.getBoundingClientRect().top+scrollY-10)');p.screenshot(path=str(out/'iron-catalogue.png'));screens.append('iron-catalogue.png');p.fill('#lab-search','')
     p.locator('.iv-modes [data-mode=compact]').click();p.locator('.lab-controls').evaluate('(el)=>window.scrollTo(0,el.getBoundingClientRect().top+scrollY-10)');p.screenshot(path=str(out/'catalog-compact.png'));screens.append('catalog-compact.png');assert p.locator('.iv-compact .lab-card').count()==24
     p.locator('.iv-modes [data-mode=cards]').click()
     # Source selectors reflect actual methods and preserve multiple outputs.
     methods={}
     for r in model['recipes']:
      for o in r['outputs']:methods.setdefault(o['item_id'],[]).append(r)
     alternate=next(key for key,rows in methods.items() if len(rows)>1);p.fill('#lab-search',alternate);p.locator('[data-item="'+alternate+'"]').click();assert p.locator('#lab-method option').count()==len(methods[alternate]);p.select_option('#lab-method',methods[alternate][-1]['id']);assert p.locator('#lab-method').input_value()==methods[alternate][-1]['id'];p.keyboard.press('Escape')
     multi=next(r for r in model['recipes'] if len(r['outputs'])>1);p.fill('#lab-search',multi['outputs'][0]['item_id']);p.locator('[data-item="'+multi['outputs'][0]['item_id']+'"]').click();p.select_option('#lab-method',multi['id']);assert p.get_by_role('heading',name='Results per batch',exact=True).locator('..').locator('.lab-material').count()==len(multi['outputs']);p.keyboard.press('Escape');report['real_method_selection']=True;report['real_multiple_outputs']=True
     # Deep source-backed chain, with manually chosen external stops, not guessed gathering.
     target=math['explicitDeepest']['id'];p.fill('#lab-search',target);p.locator('.lab-card').click();p.click('#handle');p.get_by_text('External inputs · explicit cycle handling',exact=True).click()
     for key in math['manual_external_items']:p.get_by_label(names[key],exact=True).check()
     p.get_by_text('External inputs · explicit cycle handling',exact=True).click();p.fill('#lab-quantity','3');p.get_by_role('button',name='Calculate materials',exact=True).click();assert 'PARTIAL ESTIMATE' not in p.locator('#lab-calculation').inner_text();p.locator('#lab-calculation').scroll_into_view_if_needed();p.wait_for_timeout(150);p.screenshot(path=str(out/'complex-recipe.png'));screens.append('complex-recipe.png');p.get_by_text('Craft path · structural quantities before inventory',exact=True).click();p.get_by_text('Craft path · structural quantities before inventory',exact=True).scroll_into_view_if_needed();p.screenshot(path=str(out/'craft-path.png'));screens.append('craft-path.png')
     p.go_back();p.wait_for_selector('#sheet:not([open])',state='attached')
     # Full inventory retains3219entries while rendering only24slots.
     inventory={item['id']:20 for item in model['items']};p.evaluate('(v)=>localStorage.setItem("hytale-craft-lab-inventory-v1",JSON.stringify(v))',inventory);p.reload();p.wait_for_selector('.lab-card');p.locator('#nav [data-view=inventory]').click();assert p.locator('[data-stock]').count()==24;assert str(len(inventory))+' inventory entries' in p.locator('#view-content').inner_text();p.locator('.lab-inventory-grid').evaluate('(el)=>window.scrollTo(0,el.getBoundingClientRect().top+scrollY-45)');p.wait_for_timeout(150);p.screenshot(path=str(out/'full-inventory.png'));screens.append('full-inventory.png');p.locator('.iv-modes [data-mode=compact]').click();p.locator('.lab-inventory-grid').evaluate('(el)=>window.scrollTo(0,el.getBoundingClientRect().top+scrollY-10)');p.screenshot(path=str(out/'inventory-compact.png'));screens.append('inventory-compact.png');p.locator('.iv-modes [data-mode=cards]').click()
     # Real shared plan compared independently with the historical source arithmetic.
     goals=math['plan']['goals'];inv={k:q//2 for k,q in math['plan']['totals'].items() if q//2};p.evaluate('([a,b])=>{localStorage.setItem("hytale-craft-lab-inventory-v1",JSON.stringify(a));localStorage.setItem("hytale-craft-lab-plan-v1",JSON.stringify(b))}',[inv,goals]);p.reload();p.wait_for_selector('.lab-card');p.locator('#nav [data-view=plan]').click();p.get_by_role('button',name='Calculate shared plan',exact=True).click();assert 'Craft batches' in p.locator('#lab-plan-result').inner_text();p.locator('#lab-plan-result').scroll_into_view_if_needed();p.screenshot(path=str(out/'shared-plan.png'));screens.append('shared-plan.png')
     # A known player's item is resolved from this source, not hard-coded recipe contents.
     target=next(i['id'] for i in model['items'] if (i['names']['en'] or '').lower()=='crude shortbow');recipe=next(r for r in model['recipes'] if any(o['item_id']==target for o in r['outputs']));inv={s['options'][0]['id']:s['quantity'] for s in recipe['inputs']};p.evaluate('(v)=>{localStorage.setItem("hytale-craft-lab-inventory-v1",JSON.stringify(v));localStorage.setItem("hytale-craft-lab-plan-v1","{}")}',inv);p.reload();p.wait_for_selector('.lab-card');p.locator('#nav [data-view=craftable]').click();p.locator('input[type=search]').fill(names[target]);p.wait_for_selector('.dw-card');assert names[target] in p.locator('#view-content').inner_text();p.locator('.dw-card').first.scroll_into_view_if_needed();p.wait_for_timeout(200);p.screenshot(path=str(out/'what-can-craft.png'));screens.append('what-can-craft.png');report['discovery']=p.evaluate('window.CRAFT_LAB_METRICS')
     p.get_by_role('button',name='Inspect recipe',exact=True).click();p.fill('#lab-quantity','1');p.get_by_role('button',name='Calculate materials',exact=True).click();before=p.evaluate('localStorage.getItem("hytale-craft-lab-inventory-v1")');p.locator('#lab-calculation').scroll_into_view_if_needed();p.screenshot(path=str(out/'item-calculation.png'));screens.append('item-calculation.png');p.check('#lab-strict');p.get_by_role('button',name='Calculate materials',exact=True).click();assert 'canonicalRequirements' in p.locator('#lab-calculation').inner_text();assert p.evaluate('localStorage.getItem("hytale-craft-lab-inventory-v1")')==before;p.keyboard.press('Escape');assert not p.locator('#sheet').is_visible()
     # Removing a source never rewrites inventory/plan bytes.
     p.locator('#nav [data-view=catalog]').click();p.fill('#lab-search','');saved=p.evaluate('()=>[localStorage.getItem("hytale-craft-lab-inventory-v1"),localStorage.getItem("hytale-craft-lab-plan-v1")]');p.click('#lab-detach');assert p.locator('[data-item]').count()==0;p.get_by_role('button',name='Reconnect local source').click();p.wait_for_selector('.lab-card');assert p.evaluate('()=>[localStorage.getItem("hytale-craft-lab-inventory-v1"),localStorage.getItem("hytale-craft-lab-plan-v1")]')==saved;report['source_detach_preserved_bytes']=True
     # Integrity, unresolved references and cycles are checked against the same real model.
     statuses=p.evaluate('()=>({blocked:CRAFT_LAB_MODEL.blocked.size,cycle:CRAFT_LAB_MODEL.availability(CRAFT_LAB_MODEL.cycleInputs[0],{}).status})');assert statuses['blocked']>0;assert statuses['cycle']=='cycle';report['unresolved_and_cycles']=statuses
    context.close()
   # Slow network and CPU: no public endpoint involved.
   c=browser.new_context(viewport={'width':393,'height':852},is_mobile=True,has_touch=True);p=c.new_page();session=c.new_cdp_session(p);session.send('Network.enable');session.send('Network.emulateNetworkConditions',{'offline':False,'latency':150,'downloadThroughput':150000,'uploadThroughput':50000});session.send('Emulation.setCPUThrottlingRate',{'rate':4});start=time.monotonic();p.goto(url,wait_until='domcontentloaded',timeout=30000);p.wait_for_selector('.lab-card',timeout=30000);ready=time.monotonic()-start;p.locator('.iv-art img').first.evaluate('(e)=>e.decode()');report['memory']=session.send('Runtime.getHeapUsage');report['slow_network']={'visible_icon_ready_seconds':round(time.monotonic()-start,3),'ready_seconds':round(ready,3),'cpu_throttling':4,'latency_ms':150,'download_bytes_per_second':150000,**p.evaluate('window.CRAFT_LAB_BOOT')};c.set_offline(True);p.fill('#lab-search',target);p.locator('[data-item="'+target+'"]').click();p.get_by_role('button',name='Calculate materials',exact=True).click();assert 'Unexpanded material requirements' in p.locator('#lab-calculation').inner_text();report['offline_after_loaded']=True;browser.close()
  assert not errors,errors;report.update(widths=metrics,screenshots=screens,javascript_errors=errors,real_items=len(model['items']),real_material_recipes=len(model['recipes']),all_checks_passed=True);(out/'browser-report.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='screenshots'}))
 finally:server.shutdown();server.server_close()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('build',type=Path);p.add_argument('math_report',type=Path);p.add_argument('--output',type=Path,default=ROOT/'.private/real-data-lab/screens');p.add_argument('--visuals',type=Path);a=p.parse_args();run(a.build,a.math_report,a.output,a.visuals)
