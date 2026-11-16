/* Shared game panels. UI state is derived; saved inventory/projects stay in existing formats. */
(function(root){'use strict';
const previews=new Map();
const el=(tag,text,cls)=>{const x=document.createElement(tag);if(text!==undefined)x.textContent=text;if(cls)x.className=cls;return x};
function icon(id){const key=id.startsWith('lesson:')?id.slice(7):null;return ['blade','pick','panel','strip','fibre','stone','wood'].includes(key)?'assets/learning-items/'+key+'.webp':'assets/ui-v2/nav-plan.webp'}
function image(id){const im=el('img');const path=icon(id),key=path.startsWith('assets/learning-items/')?'item-'+id.slice(7):'nav-plan';im.src=root.CRAFT_BETA_IMAGES?.[key]||path;im.alt='';im.width=110;im.height=110;im.loading='lazy';return im}
function badge(s,ok=false){return el('span',s,'dw-badge'+(ok?' success':''))}
function btn(s,fn,cls){const b=el('button',s,cls);b.type='button';b.onclick=fn;return b}
function slot(id,q,c){const box=el('div',undefined,'dw-slot');box.append(image(id),el('strong',c.name(id)),el('span','× '+q,'dw-count'));return box}
function heading(host,c,title,desc){host.classList.add('dw-view');const h=el('section',undefined,'dw-hero');h.append(el('span',c.t('dwEyebrow'),'dw-eyebrow'),el('h3',title),el('p',desc));h.append(badge(c.t(c.scope==='demo'?'tutorialShort':'user')));host.append(h);return h}
function section(host,title){const s=el('section',undefined,'dw-panel');s.append(el('h3',title));host.append(s);return s}
function empty(host,c,key){const d=el('div',undefined,'dw-empty');d.append(image('none'),el('p',c.t(key)));host.append(d)}
function path(host,c,id,q=1){
 const outer=el('details');outer.append(el('summary',c.t('dwPath')));host.append(outer);
 try{const tree=root.CraftWorkspace.dependencyTree(c.db,id,q);function branch(v,depth){const card=el(v.raw?'div':'details',undefined,'dw-node');if(!v.raw){card.open=depth<1;card.append(el('summary',c.name(v.id)+' × '+v.quantity))}const link=btn('',()=>c.open(v.id),'dw-path-link');link.append(image(v.id),el('span',c.name(v.id)+' × '+v.quantity));card.append(link);if(!v.raw){card.append(el('small',c.t('crafts')+': '+v.batches+' · '+c.t('yield')+': '+v.produced));if(depth<8)for(const ch of v.children)card.append(branch(ch,depth+1));else card.append(el('p',c.t('dwMoreDepth')))}return card}outer.append(el('p',c.t('treeBeforeInventory'),'muted'),branch(tree,0))}catch(e){outer.append(el('p',c.t('cycle'),'warning'))}
}
function detail(host,id,c){
 const r=c.db[id],hero=heading(host,c,c.name(id),c.t(r?'dwItemIntro':'dwRawIntro'));const h=el('div',undefined,'dw-item-head');h.append(slot(id,r?.yield||1,c));const b=el('div');b.append(badge(c.t(r?'dwRecipe':'rawMaterial')),el('p',c.t(r?'dwMaterialCheck':'dwNoConfirmed')));h.append(b);hero.append(h);
 const model=root.Craftable.prepare(c.db);
 if(r){const s=section(host,c.t('ingredients')),grid=el('div',undefined,'dw-grid');for(const [key,q] of Object.entries(r.ingredients)){const card=slot(key,q,c),b=btn(c.t('dwInspect'),()=>c.open(key));card.append(b);grid.append(card)}s.append(grid);path(host,c,id)}
 const station=section(host,c.t('workstations'));const names=root.CraftWorkspace.stationNames(r);if(names.length)for(const name of names)station.append(badge(name));else station.append(el('p',c.t(c.scope==='demo'?'noStation':'noSavedStations'),'muted'));
 const used=section(host,c.t('dwUsedIn')),ids=model.usedIn(id);if(!ids.length)used.append(el('p',c.t('dwNoUses'),'muted'));for(const target of ids.slice(0,30)){const b=btn('',()=>c.open(target),'dw-path-link');b.append(image(target),el('span',c.name(target)));used.append(b)}if(ids.length>30)used.append(el('p',c.t('dwLimited')));
 const notes=el('details',undefined,'dw-help');notes.append(el('summary',c.t('dwProvenance')),el('p',c.t(c.scope==='demo'?'tutorial':'sourceOwn'),'warning'),el('p',r?.source||c.t(c.scope==='demo'?'dwOriginal':'dwNoConfirmed')),el('code',id,'dw-meta'));host.append(notes);
}
function craftable(host,c){
 heading(host,c,c.t('craftable'),c.t('dwIntro'));host.append(el('p',c.t(c.scope==='demo'?'tutorial':'sourceOwn'),'warning'));
 let inventory,raw=c.inventoryRaw();try{inventory=root.CraftWorkspace.parseLines(raw)}catch{empty(host,c,'dwBrokenInventory');host.append(btn(c.t('inventory'),c.inventory));return}
 let model;try{model=root.Craftable.prepare(c.db)}catch{empty(host,c,'recipeError');return}
 const selected=new Set((previews.get(c.scope)||[]).filter(id=>Object.hasOwn(c.db,id))),summary=section(host,c.t('dwSummary')),inventorySection=el('details');inventorySection.open=!Object.keys(inventory).length;inventorySection.append(el('summary',c.t('inventory')+' · '+Object.keys(inventory).length));host.append(inventorySection);const results=section(host,c.t('dwAvailable')),combined=section(host,c.t('dwTogether'));
 const invSearch=el('input');invSearch.type='search';invSearch.placeholder=c.t('dwFindMaterial');invSearch.setAttribute('aria-label',c.t('dwFindMaterial'));inventorySection.append(invSearch);const invGrid=el('div',undefined,'dw-grid');inventorySection.append(invGrid);
 const allIds=[...new Set([...Object.keys(inventory),...Object.values(c.db).flatMap(r=>Object.keys(r.ingredients)),...model.ids])];let invLimit=12,showAll=!Object.keys(inventory).length;
 function adjust(id,delta){const next=Object.assign(Object.create(null),inventory);next[id]=Math.max(0,(next[id]||0)+delta);if(next[id]>999999){c.notify('limit');return}if(!next[id])delete next[id];const value=Object.entries(next).map(([k,q])=>k+': '+q).join('\n');if(c.saveInventory(value,raw)){raw=value;inventory=next;inventorySection.querySelector('summary').textContent=c.t('inventory')+' · '+Object.keys(inventory).length;drawInventory();schedule()}}
 function drawInventory(){invGrid.replaceChildren();const query=invSearch.value.toLocaleLowerCase();const ids=allIds.filter(id=>(showAll||query||inventory[id]>0)&&(!query||c.name(id).toLocaleLowerCase().includes(query)||id.toLowerCase().includes(query)));for(const id of ids.slice(0,invLimit)){const card=slot(id,inventory[id]||0,c),actions=el('div',undefined,'dw-actions');for(const [label,delta] of [['−',-1],['+',1]]){const b=btn(label,()=>{adjust(id,delta);invGrid.querySelector('[data-control="'+CSS.escape(id+label)+'"]')?.focus({preventScroll:true})});b.dataset.control=id+label;b.setAttribute('aria-label',c.t(delta>0?'dwAdd':'dwRemove')+' '+c.name(id));b.disabled=delta<0&&!inventory[id];actions.append(b)}card.append(actions);invGrid.append(card)}if(ids.length>invLimit)invGrid.append(btn(c.t('dwMore'),()=>{invLimit+=12;drawInventory()},'dw-load'))}
 invSearch.oninput=()=>{invLimit=12;drawInventory()};drawInventory();inventorySection.append(btn(c.t('dwAddMaterials'),()=>{showAll=true;drawInventory();invSearch.focus()}),btn(c.t('dwExactInventory'),c.inventory));
 results.append(el('p',c.t('dwSeparate'),'warning'));const search=el('input');search.type='search';search.placeholder=c.t('searchRecipes');search.setAttribute('aria-label',c.t('searchRecipes'));results.append(search);
 const tabs=el('div',undefined,'dw-tabs'),list=el('div'),status=el('p',undefined,'dw-live');status.setAttribute('role','status');let filter='available',limit=12,ticket=0;results.append(tabs,status,list);
 for(const [key,label] of [['available','dwAvailable'],['direct','dwDirect'],['chain','dwChain'],['all','dwAll']]){const b=btn(c.t(label),()=>{filter=key;limit=12;for(const x of tabs.children)x.setAttribute('aria-pressed',String(x===b));schedule()});b.setAttribute('aria-pressed',String(key===filter));tabs.append(b)}
 function drawCombined(){combined.replaceChildren(el('h3',c.t('dwTogether')),el('p',c.t('dwTogetherHint'),'muted'));if(!selected.size){combined.append(el('p',c.t('dwChooseGoals')));return}try{const goals=Object.fromEntries([...selected].map(id=>[id,1])),v=model.together(goals,inventory);combined.append(el('p',c.t(v.available?'dwTogetherYes':'dwTogetherNo'),'warning'));for(const [id,q] of Object.entries(goals))combined.append(btn(c.t('dwUnselect')+' · '+c.name(id)+' × '+q,()=>{selected.delete(id);previews.set(c.scope,[...selected]);schedule()}));const output=el('div');c.result(output,v);combined.append(output)}catch(e){combined.append(el('p',c.t('cycle'),'warning'))}}
 function schedule(){const request=++ticket;status.textContent=c.t('dwChecking');setTimeout(()=>{if(!host.isConnected||request!==ticket)return;draw()},25)}
 function draw(){
  list.replaceChildren();const query=search.value.toLocaleLowerCase(),ids=model.ids.filter(id=>!query||c.name(id).toLocaleLowerCase().includes(query)||id.toLowerCase().includes(query));let count=0,available=0,unknown=0,shown=0,examined=0;const maxScan=500;
  for(const id of ids.slice(0,maxScan)){
   let row;try{row=model.capacity(id,inventory)}catch{row={id,status:'unknown',maximum:0}}
   examined++;if(row.status==='unknown')unknown++;if(row.status==='direct'||row.status==='chain')available++;
   if(filter==='available'&&!row.maximum||filter==='direct'&&row.status!=='direct'||filter==='chain'&&row.status!=='chain')continue;count++;if(shown++>=limit)continue;
   const card=el('article',undefined,'dw-card');card.dataset.craftable=id;const head=el('div',undefined,'dw-card-top'),title=el('div');title.append(el('h3',c.name(id)),badge(c.t('dw'+row.status[0].toUpperCase()+row.status.slice(1)),!!row.maximum));head.append(image(id),title);card.append(head,el('p',c.t('dwMaximum')+': '+(row.capped?'≥ ':'')+row.maximum,'dw-capacity'));
   const actions=el('div',undefined,'dw-actions');actions.append(btn(c.t('dwInspect'),()=>c.open(id)));const choose=btn(c.t(selected.has(id)?'dwUnselect':'dwSelect'),()=>{selected.has(id)?selected.delete(id):selected.add(id);previews.set(c.scope,[...selected]);drawCombined();schedule()});choose.setAttribute('aria-pressed',String(selected.has(id)));actions.append(choose);card.append(actions);if(row.result){const remain=el('details');remain.append(el('summary',c.t('dwAfterOne')));const preview=el('div');c.result(preview,row.result);remain.append(preview);card.append(remain)}path(card,c,id);list.append(card);
  }
  if(!count)empty(list,c,'dwNoCrafts');if(count>limit)list.append(btn(c.t('dwMore'),()=>{limit+=12;schedule()},'dw-load'));
  status.textContent=c.t('dwChecked')+' '+examined+(ids.length>maxScan?' · '+c.t('dwLimited'):'');summary.replaceChildren(el('h3',c.t('dwSummary')));const grid=el('div',undefined,'dw-summary');for(const [value,key] of [[Object.keys(inventory).length,'dwStockKinds'],[available,'dwAvailable']]){const cell=el('div');cell.append(el('strong',String(value)),el('span',c.t(key)));grid.append(cell)}summary.append(grid,el('p',c.t('dwMaterialCheck'),'muted'));if(unknown)summary.append(el('p',c.t('dwUnknown')+': '+unknown,'warning'));drawCombined();
 }
 search.oninput=()=>{limit=12;schedule()};drawCombined();schedule();
}
function decorateResult(host,value){host.classList.add('dw-result');const rows=[...host.querySelectorAll('.row')];let i=0;for(const map of [value.totals,value.steps,value.stock])for(const [id,q] of Object.entries(map))if(q>0)rows[i++]?.prepend(image(id))}
root.CraftDeepUI={detail,craftable,path,image,slot,decorateResult};
})(globalThis);
