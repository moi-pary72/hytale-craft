/* Public ID catalog is separate from local recipes. Missing data stays missing. */
(()=>{'use strict';
const $=id=>document.getElementById(id),ru=()=>$('language').value==='ru',t=(en,r)=>ru()?r:en;
const section=document.createElement('section');section.className='card';section.style='max-width:760px;margin:18px auto';
section.style.overflowWrap='anywhere';
section.innerHTML='<h2 id="game-title"></h2><p id="game-status" class="muted" role="status"></p><input id="game-search" type="search"><select id="game-category"></select><div id="game-items"></div><button id="game-more" class="secondary" type="button"></button><div id="game-card" tabindex="-1" aria-live="polite"></div>';
$('goal-home').after(section);
let data=null,limit=20,selected=null;
const cats=[['all','All','Все'],['weapons','Weapons','Оружие'],['armor','Armor','Броня'],['tools','Tools','Инструменты'],['building','Building','Строительство'],['food','Food','Еда'],['benches','Stations','Станции'],['decor','Furniture','Мебель'],['farming','Plants','Растения'],['other','Other','Другое']];
function card(item){selected=item;$('game-card').replaceChildren();const h=document.createElement('h3');h.textContent=item.id;const info=document.createElement('p');info.className='status';info.textContent=t('No confirmed recipe is available. Ingredients, yield and station are unknown. Calculation is unavailable.','Подтверждённого рецепта нет. Ингредиенты, выход и станция неизвестны. Расчёт недоступен.');const note=document.createElement('p');note.className='muted';note.textContent=t('Original game ID. Official English and Russian names were not supplied. Source: OpenHytale; generated ','Оригинальный игровой ID. Официальные английское и русское названия не предоставлены. Источник: OpenHytale; дата набора ')+data.source_generated_at+t('. Game version unknown.','. Версия игры неизвестна.');$('game-card').append(h,info,note);$('game-card').focus();}
function render(){
 $('game-title').textContent=t('📚 Game item catalog','📚 Каталог игровых предметов');$('game-search').placeholder=t('Search game IDs…','Поиск по игровым ID…');$('game-search').setAttribute('aria-label',$('game-search').placeholder);$('game-category').setAttribute('aria-label',t('Item category','Категория предметов'));
 const c=$('game-category').value||'all';$('game-category').replaceChildren(...cats.map(([v,en,r])=>new Option(ru()?r:en,v)));$('game-category').value=c;
 if(!data)return;
 $('game-status').textContent=t('Community ID snapshot: ','Набор ID из независимого источника: ')+data.items.length+t(' items; 0 confirmed recipes. Source date: ',' предметов; 0 подтверждённых рецептов. Дата источника: ')+data.source_generated_at;
 const q=$('game-search').value.trim().toLowerCase();const found=data.items.filter(i=>(c==='all'||i.category===c)&&i.id.toLowerCase().includes(q));$('game-items').replaceChildren();
 for(const i of found.slice(0,limit)){const b=document.createElement('button');b.type='button';b.className='catalog-result';b.style.overflowWrap='anywhere';b.textContent=i.id;b.onclick=()=>card(i);$('game-items').append(b)}
 if(!found.length)$('game-items').textContent=t('No matching items.','Предметы не найдены.');$('game-more').hidden=found.length<=limit;$('game-more').textContent=t('Show more','Показать ещё')+' ('+Math.max(0,found.length-limit)+')';if(selected)cardWithoutFocus();
}
function cardWithoutFocus(){const active=document.activeElement;card(selected);active?.focus()}
$('game-search').oninput=()=>{limit=20;render()};$('game-category').onchange=()=>{limit=20;render()};$('game-more').onclick=()=>{limit+=40;render()};$('language').addEventListener('change',render);
// Goals now open the actual ID catalog; local recipes remain available in the planner.
$('goal-go').addEventListener('click',()=>{if(!data)return;const c=$('goal-detail').value;if(cats.some(x=>x[0]===c)){$('goal-results')?.replaceChildren();$('game-category').value=c;$('game-search').value='';limit=20;render();section.scrollIntoView({block:'start',behavior:'smooth'})}});
render();$('game-status').textContent=t('Loading catalog…','Загрузка каталога…');
fetch('data/catalog.json').then(r=>{if(!r.ok)throw Error(r.status);return r.json()}).then(d=>{if(d.schema_version!==1||!Array.isArray(d.items)||d.items.some(i=>typeof i.id!=='string'))throw Error('Invalid catalog');data=d;render()}).catch(()=>{$('game-status').textContent=t('Catalog unavailable. Your saved recipes remain available in advanced tools.','Каталог недоступен. Сохранённые рецепты доступны в дополнительных инструментах.')});
})();
