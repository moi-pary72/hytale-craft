/* Original visual assets, independent of every catalogue and user storage schema. */
(function(root){'use strict';
const tiles=['sword','axe','pickaxe','helmet','breastplate','wood','stone','metal','fabric','plant','food','alchemy','furniture','building','station','neutral'];
const lessons=new Set(['blade','pick','strip','panel','fibre','stone','wood']);
const labels={en:{category:'Category illustration',neutral:'Image unavailable',individual:'Original demo illustration',cards:'Beautiful cards',compact:'Compact inventory'},ru:{category:'Иллюстрация категории',neutral:'Изображение неизвестно',individual:'Оригинальная учебная иллюстрация',cards:'Красивые карточки',compact:'Компактный инвентарь'},es:{category:'Ilustración de categoría',neutral:'Imagen no disponible',individual:'Ilustración de demostración original',cards:'Tarjetas ilustradas',compact:'Inventario compacto'},'pt-BR':{category:'Ilustração de categoria',neutral:'Imagem indisponível',individual:'Ilustração original de demonstração',cards:'Cartões ilustrados',compact:'Inventário compacto'}};
function category(item={}){
 const v=String(item.id||'')+' '+String(item.names?.en||item.name||'')+' '+String(item.category||'');
 // Conservative silhouette families. Unknown ore, bows, boots and magical items stay neutral.
 for(const [key,re] of [['pickaxe',/pickaxe/i],['axe',/(?:^|[\s_:])(?:battle)?axe(?:$|[\s_:])/i],['sword',/sword/i],['helmet',/helmet|helm(?:$|[\s_:])/i],['breastplate',/breastplate|cuirass|chestplate/i],['wood',/(?:^|[\s_:])(?:wood|timber|log)(?:$|[\s_:])/i],['metal',/ingot/i],['fabric',/cloth|fabric|linen|wool/i],['plant',/flower|petal|herb|seed|sapling/i],['food',/cooked|meal|soup|stew|bread|food/i],['alchemy',/potion|alchemy/i],['furniture',/chair|furniture/i],['building',/brick|building|masonry/i],['station',/workbench|craftingbench|bench_/i],['stone',/(?:^|[\s_:])(?:stone|rock)(?:$|[\s_:])/i]])if(re.test(v))return key;
 return 'neutral';
}
function resolve(item={}){const id=String(item.id||''),key=id.startsWith('lesson:')?id.slice(7):'';
 if(lessons.has(key))return {level:'individual',key,path:'assets/learning-items/'+key+'.webp',official:false};
 const family=category(item);return {level:family==='neutral'?'neutral':'category',key:family,tile:tiles.indexOf(family),path:'assets/item-system/categories.webp',official:false};
}
function image(item={},lang='en'){
 const visual=resolve(item),words=labels[lang]||labels.en,box=document.createElement('span'),im=document.createElement('img');box.className='iv-art';box.dataset.visual=visual.level;box.dataset.family=visual.key;box.setAttribute('role','img');box.setAttribute('aria-label',words[visual.level]||words.neutral);box.title=box.getAttribute('aria-label');im.alt='';im.loading='lazy';im.decoding='async';
 function apply(v){box.className='iv-art'+(v.tile!==undefined?' iv-sprite iv-x'+v.tile%4+' iv-y'+Math.floor(v.tile/4):'');im.src=root.CRAFT_BETA_IMAGES?.[v.tile!==undefined?'categories':'item-'+v.key]||v.path;}
 apply(visual);let failed=false;im.onerror=()=>{if(failed){im.remove();box.classList.add('iv-failed');return}failed=true;box.dataset.visual='neutral';box.dataset.family='neutral';box.setAttribute('aria-label',words.neutral);apply({tile:15,path:'assets/item-system/categories.webp'})};box.append(im);return box;
}
function readMode(){try{return localStorage.getItem('hytale-craft-item-view-v1')==='compact'?'compact':'cards'}catch{return 'cards'}}
function modeControl(host,grid,lang='en'){const words=labels[lang]||labels.en,bar=document.createElement('div');bar.className='iv-modes';bar.setAttribute('role','group');bar.setAttribute('aria-label',words.compact+' / '+words.cards);let mode=readMode();function draw(){grid.classList.toggle('iv-compact',mode==='compact');grid.dataset.itemView=mode;for(const b of bar.children)b.setAttribute('aria-pressed',String(b.dataset.mode===mode))}for(const key of ['cards','compact']){const b=document.createElement('button');b.type='button';b.dataset.mode=key;b.textContent=words[key];b.onclick=()=>{mode=key;try{localStorage.setItem('hytale-craft-item-view-v1',mode)}catch{}draw()};bar.append(b)}host.append(bar);draw();return bar}
root.CraftItemVisuals={resolve,category,image,modeControl,labels,tiles};if(typeof module!=='undefined')module.exports=root.CraftItemVisuals;
})(globalThis);
