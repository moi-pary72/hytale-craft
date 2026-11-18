/* Owner-supplied, local-only catalogue reader. No requests, persistence or uploads. */
(function(root){'use strict';
const LIMIT=12*1024*1024,PAGE_SIZE=36,MAX_ITEMS=15000,MAX_RECIPES=20000;
const plain=x=>x!==null&&typeof x==='object'&&!Array.isArray(x),safeId=id=>typeof id==='string'&&id.length>0&&id.length<180&&!['__proto__','constructor','prototype'].includes(id);
function parse(value){
 if(!plain(value)||!plain(value.canonical)||!Array.isArray(value.canonical.items)||!Array.isArray(value.canonical.recipes))throw Error('Нужен файл каталога с canonical.items и canonical.recipes.');
 const items=value.canonical.items,recipes=value.canonical.recipes;
 if(items.length>MAX_ITEMS||recipes.length>MAX_RECIPES)throw Error('Файл превышает допустимый размер каталога.');
 const byId=new Map(),byOutput=new Map(),categories=new Set();
 for(const raw of items){if(!plain(raw)||!safeId(raw.id)||byId.has(raw.id))throw Error('Некорректный или повторяющийся ID предмета.');
  const name=plain(raw.names)?Object.values(raw.names).find(v=>typeof v==='string'&&v.trim())||raw.id:raw.id;
  const item={id:raw.id,name:String(name).slice(0,200),category:typeof raw.category==='string'?raw.category.slice(0,90):'Другое'};
  byId.set(item.id,item);categories.add(item.category);
 }
 for(const r of recipes){if(!plain(r)||!safeId(r.id)||!safeId(r.primary_output)||!Array.isArray(r.inputs)||!Array.isArray(r.outputs))continue;
  if(!byId.has(r.primary_output))continue;
  if(!byOutput.has(r.primary_output))byOutput.set(r.primary_output,[]);
  byOutput.get(r.primary_output).push(r);
 }
 const sorted=[...byId.values()].sort((a,b)=>a.name.localeCompare(b.name,'ru'));
 return {byId,byOutput,items:sorted,categories:[...categories].sort((a,b)=>a.localeCompare(b,'ru')),recipeCount:[...byOutput.values()].reduce((n,rs)=>n+rs.length,0)};
}
function search(model,query='',category='',offset=0){const term=String(query).normalize('NFKC').toLocaleLowerCase().trim(),matches=model.items.filter(x=>(!category||x.category===category)&&(!term||(x.id+' '+x.name).normalize('NFKC').toLocaleLowerCase().includes(term)));const start=Math.max(0,Math.floor(offset)||0);return {count:matches.length,items:matches.slice(start,start+PAGE_SIZE),page:Math.floor(start/PAGE_SIZE)+1,pages:Math.max(1,Math.ceil(matches.length/PAGE_SIZE))};}
function displayName(model,id){return model.byId.get(id)?.name||id;}
function inputRows(model,recipe){const rows=[];for(const input of recipe.inputs||[]){if(!plain(input)||!Array.isArray(input.options))continue;const options=input.options.filter(o=>plain(o)&&safeId(o.id)).map(o=>displayName(model,o.id));if(!options.length)continue;const quantity=Number.isSafeInteger(input.quantity)&&input.quantity>0?String(input.quantity):'?';rows.push(options.join(' / ')+' × '+quantity);}return rows;}
function el(tag,content,className){const node=document.createElement(tag);if(content!==undefined)node.textContent=content;if(className)node.className=className;return node;}
function init(){const file=document.getElementById('catalog-file'),status=document.getElementById('status'),browser=document.getElementById('browser'),q=document.getElementById('query'),cat=document.getElementById('category'),results=document.getElementById('results'),stats=document.getElementById('stats'),detail=document.getElementById('detail'),prev=document.getElementById('prev'),next=document.getElementById('next'),page=document.getElementById('page');let model=null,offset=0;
 function draw(){if(!model)return;const found=search(model,q.value,cat.value,offset);if(offset>0&&found.page>found.pages){offset=(found.pages-1)*PAGE_SIZE;return draw()}results.replaceChildren();for(const item of found.items){const b=el('button',undefined,'item');b.type='button';b.append(el('strong',item.name),el('small',item.category+' · '+item.id),el('small','Рецептов: '+(model.byOutput.get(item.id)?.length||0)));b.onclick=()=>openItem(item.id);results.append(b)}if(!found.count)results.append(el('p','Ничего не найдено.'));page.textContent=found.count+' найдено · страница '+found.page+' / '+found.pages;prev.disabled=offset===0;next.disabled=found.page>=found.pages;}
 function openItem(id){detail.replaceChildren();const item=model.byId.get(id);if(!item)return;const close=el('button','Закрыть карточку','close');close.onclick=()=>{detail.hidden=true;detail.replaceChildren()};detail.append(close,el('h2',item.name),el('p','ID: '+item.id),el('p','Категория: '+item.category));const recipes=model.byOutput.get(id)||[];if(!recipes.length)detail.append(el('p','В этом файле нет структурно распознанного рецепта.'));for(const r of recipes){const box=el('section',undefined,'method');box.append(el('strong','Метод: '+r.id));const outs=(r.outputs||[]).filter(x=>plain(x)&&safeId(x.item_id)).map(x=>displayName(model,x.item_id)+' × '+(Number.isSafeInteger(x.quantity)&&x.quantity>0?x.quantity:'?'));box.append(el('p','Выход: '+(outs.join(' + ')||'неизвестен')));const inputs=inputRows(model,r);if(inputs.length){const list=el('ul');for(const s of inputs)list.append(el('li',s));box.append(list)}else box.append(el('p','Состав не указан.'));const benches=r.station_requirements?.entries||[];if(Array.isArray(benches)&&benches.length)box.append(el('p','Станции: '+benches.map(b=>typeof b.station_id==='string'?b.station_id:'не указано').join(' / ')));box.append(el('p','Не подтверждено для текущей версии Hytale.','hint'));detail.append(box)}detail.hidden=false;detail.scrollIntoView({block:'start',behavior:'smooth'});}
 file.onchange=async()=>{const selected=file.files?.[0];if(!selected)return;model=null;browser.hidden=true;detail.hidden=true;detail.replaceChildren();if(selected.size>LIMIT){status.textContent='Ошибка: файл больше 12 МБ.';return}try{const raw=await selected.text();model=parse(JSON.parse(raw));if(!model.items.length)throw Error('Каталог пуст.');cat.replaceChildren(new Option('Все категории',''));for(const c of model.categories)cat.add(new Option(c,c));stats.replaceChildren(el('span',model.items.length+' предметов'),el('span',model.recipeCount+' методов'),el('span','Только локальный просмотр'));q.value='';offset=0;browser.hidden=false;status.textContent='Файл прочитан локально. В сеть не отправлялся.';draw()}catch(err){status.textContent='Не удалось открыть каталог: '+(err?.message||'ошибка формата');model=null;}};
 q.oninput=cat.onchange=()=>{offset=0;detail.hidden=true;draw()};prev.onclick=()=>{offset=Math.max(0,offset-PAGE_SIZE);draw()};next.onclick=()=>{offset+=PAGE_SIZE;draw()};
}
root.CraftLocalCatalog={parse,search,inputRows,displayName};if(typeof module!=='undefined'&&module.exports)module.exports=root.CraftLocalCatalog;
if(typeof document!=='undefined')document.addEventListener('DOMContentLoaded',init);
})(globalThis);