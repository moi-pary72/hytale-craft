/* Original visual assets, independent of every catalogue and user storage schema. */
(function(root){'use strict';
const tiles=['sword','axe','pickaxe','helmet','breastplate','wood','stone','metal','fabric','plant','food','alchemy','furniture','building','station','neutral'];
const extendedTiles=['bow','dagger','hammer','shield','ore','coal','leather','fibre','boots','gauntlets','leggings','chest','cauldron','furnace','anvil','crystal'];
let research=new Map(),researchEnabled=false;
const lessons=new Set(['blade','pick','strip','panel','fibre','stone','wood']);
const labels={en:{category:'Category illustration',neutral:'Image unavailable',individual:'Original demo illustration',cards:'Beautiful cards',compact:'Compact inventory'},ru:{category:'Иллюстрация категории',neutral:'Изображение неизвестно',individual:'Оригинальная учебная иллюстрация',cards:'Красивые карточки',compact:'Компактный инвентарь'},es:{category:'Ilustración de categoría',neutral:'Imagen no disponible',individual:'Ilustración de demostración original',cards:'Tarjetas ilustradas',compact:'Inventario compacto'},'pt-BR':{category:'Ilustração de categoria',neutral:'Imagem indisponível',individual:'Ilustração original de demonstração',cards:'Cartões ilustrados',compact:'Inventário compacto'}};
function category(item={}){
 const v=String(item.id||'')+' '+String(item.names?.en||item.name||'')+' '+String(item.category||'');
 if(/cauldron|arcade|machine|essence|crystal|gemstone|rune|(?:^|[\s_:])ore(?:$|[\s_:])/i.test(v))return 'neutral';
 if(/wood(?:en)?|stone|bone|crude|adamantite|mithril|thorium|copper|bronze|gold/i.test(v)&&/pickaxe|axe|sword|helmet|helm|cuirass|chestplate/i.test(v))return 'neutral';
 // Conservative silhouette families. Unknown ore, bows, boots and magical items stay neutral.
 for(const [key,re] of [['pickaxe',/pickaxe/i],['axe',/(?:^|[\s_:])(?:battle)?axe(?:$|[\s_:])/i],['sword',/sword/i],['helmet',/helmet|helm(?:$|[\s_:])/i],['breastplate',/breastplate|cuirass|chestplate/i],['wood',/(?:^|[\s_:])(?:wood|timber|log)(?:$|[\s_:])/i],['metal',/ingot/i],['fabric',/cloth|fabric|linen|wool/i],['plant',/flower|petal|herb|seed|sapling/i],['food',/cooked|meal|soup|stew|bread|food/i],['alchemy',/potion|alchemy/i],['furniture',/chair|furniture/i],['building',/brick|building|masonry/i],['station',/workbench|craftingbench|bench_/i],['stone',/(?:^|[\s_:])(?:stone|rock)(?:$|[\s_:])/i]])if(re.test(v))return key;
 return 'neutral';
}
function family(item={}){
 const name=String(item.id||'')+' '+String(item.names?.en||item.name||''),categoryName=String(item.category||'');
 if(/essence|rune|gemstone|crystal|rare|arcade|machine|adamantite|mithril|thorium|cobalt|onyxium/i.test(name))return 'neutral';
 if(/wood(?:en)?|bone|crude|copper|bronze|gold/i.test(name)&&/boots|gauntlets|leggings|dagger|shield/i.test(name))return 'neutral';
 if(/wood(?:en)?|bone|crude|copper|bronze|gold/i.test(name)&&/hatchet/i.test(name))return 'neutral';
 if((categoryName==='Armor'||/^Armor[_:]/i.test(String(item.id||'')))&&(/cuirass|breastplate|chestplate|(?:^|_)Chest(?:_|\s|$)/i.test(name))){if(/wood|bone|crude|copper|bronze|gold/i.test(name))return 'neutral';return 'breastplate'}
 for(const [key,re]of [['axe',/hatchet/i],['bow',/shortbow|longbow|(?:^|[\s_:])bow(?:$|[\s_:])/i],['dagger',/dagger/i],['hammer',/hammer/i],['shield',/shield/i],['ore',/(?:^|[\s_:])ore(?:$|[\s_:])/i],['coal',/charcoal|(?:^|[\s_:])coal(?:$|[\s_:])/i],['leather',/leather|hide/i],['fibre',/fibre|fiber/i],['boots',/boots|armor_iron_feet/i],['gauntlets',/gauntlet|armor_iron_hands/i],['leggings',/leggings|greaves|armor_iron_legs/i],['chest',/(?:^|[\s_:])chest(?:$|[\s_:])/i],['cauldron',/cauldron/i],['furnace',/furnace/i],['anvil',/anvil/i]])if(re.test(name))return key;
 if(categoryName==='Bench'||/^Bench_/i.test(name))return 'station';
 if(categoryName==='Food'&&/raw|fish/i.test(name)&&!/cooked|meal|stew/i.test(name))return 'neutral';
 if(categoryName==='Furniture')return 'neutral';
 if(categoryName==='Rock')return 'stone';if(categoryName==='Wood')return 'wood';if(categoryName==='Plant')return 'plant';if(categoryName==='Cloth')return 'fabric';
 // Broad Furniture/Alchemy categories must not turn beds or machines into chairs/potions.
 const result=category({...item,category:categoryName==='Furniture'||categoryName==='Alchemy'?'':categoryName});return result;
}
function configureResearch(manifest,context={}){
 const local=['127.0.0.1','localhost','[::1]'].includes(root.location?.hostname);
 if(!local||context.mode!=='local-only'||manifest?.mode!=='private-research'||manifest.source_revision!==context.source_revision||!Array.isArray(manifest.entries)||manifest.entries.length>100)return false;
 const entries=new Map();for(const e of manifest.entries){if(typeof e.item_id!=='string'||!/^research-art\/[a-z0-9-]+\.webp$/.test(e.path)||![3,4].includes(e.columns)||!Number.isInteger(e.tile)||e.tile<0||e.tile>=e.columns**2||!e.reference?.reference_url||e.reference.publication!=='private-research-only; underlying game-design rights unconfirmed')throw Error('Untrusted research visual');for(const key of ['reference_url','reference_page']){const u=new URL(e.reference[key]);if(u.protocol!=='https'+':'||u.username||u.password)throw Error('Unsafe visual reference')}entries.set(e.item_id,e)}research=entries;researchEnabled=true;return true;
}
function setResearchEnabled(value){researchEnabled=value===true&&research.size>0}
function researchEvidence(id){return researchEnabled?research.get(id)?.reference:null}
function resolve(item={}){const id=String(item.id||''),key=id.startsWith('lesson:')?id.slice(7):'';
 if(lessons.has(key))return {level:'individual',key,path:'assets/learning-items/'+key+'.webp',official:false};
 const custom=researchEnabled&&research.get(id);if(custom)return {level:'individual',key:'research',path:custom.path,tile:custom.tile,columns:custom.columns,research:true,official:false};
 const keyFamily=family(item),extended=extendedTiles.includes(keyFamily);return {level:keyFamily==='neutral'?'neutral':'category',key:keyFamily,tile:extended?extendedTiles.indexOf(keyFamily):tiles.indexOf(keyFamily),columns:4,path:'assets/item-system/'+(extended?'extended':'categories')+'.webp',official:false};
}
function image(item={},lang='en',declaredFamily){
 const key=(tiles.includes(declaredFamily)||extendedTiles.includes(declaredFamily))?declaredFamily:null,extended=extendedTiles.includes(key);const visual=key?{level:key==='neutral'?'neutral':'category',key,tile:extended?extendedTiles.indexOf(key):tiles.indexOf(key),columns:4,path:'assets/item-system/'+(extended?'extended':'categories')+'.webp',official:false}:resolve(item),words=labels[lang]||labels.en,box=document.createElement('span'),im=document.createElement('img');box.className='iv-art';box.dataset.visual=visual.level;box.dataset.family=visual.key;if(visual.research)box.dataset.research='true';box.setAttribute('role','img');box.setAttribute('aria-label',(words[visual.level]||words.neutral)+(visual.level==='category'?' · ≈':''));if(visual.research)box.setAttribute('aria-label',({en:'Original research interpretation · reference version unmatched',ru:'Исследовательская интерпретация · версия образца не совпоставлена',es:'Interpretación de investigación · versión sin confirmar','pt-BR':'Interpretação de pesquisa · versão não confirmada'}[lang]||'Research interpretation'));box.title=box.getAttribute('aria-label');im.alt='';im.loading='lazy';im.decoding='async';
 function apply(v){const columns=v.columns||4;box.className='iv-art'+(v.tile!==undefined?' iv-sprite iv-cols'+columns+' iv-x'+v.tile%columns+' iv-y'+Math.floor(v.tile/columns):'');const asset=v.path.includes('extended.webp')?'extended':v.tile!==undefined?'categories':'item-'+v.key;im.src=(v.research?null:root.CRAFT_BETA_IMAGES?.[asset])||v.path;}

 apply(visual);let failed=false;im.onerror=()=>{if(failed){im.remove();box.classList.add('iv-failed');return}failed=true;delete box.dataset.research;box.dataset.visual='neutral';box.dataset.family='neutral';box.setAttribute('aria-label',words.neutral);apply({tile:15,path:'assets/item-system/categories.webp'})};box.append(im);return box;
}
function readMode(){try{return localStorage.getItem('hytale-craft-item-view-v1')==='compact'?'compact':'cards'}catch{return 'cards'}}
function modeControl(host,grid,lang='en'){const words=labels[lang]||labels.en,bar=document.createElement('div');bar.className='iv-modes';bar.setAttribute('role','group');bar.setAttribute('aria-label',words.compact+' / '+words.cards);let mode=readMode();function draw(){grid.classList.toggle('iv-compact',mode==='compact');grid.dataset.itemView=mode;for(const b of bar.children)b.setAttribute('aria-pressed',String(b.dataset.mode===mode))}for(const key of ['cards','compact']){const b=document.createElement('button');b.type='button';b.dataset.mode=key;b.textContent=words[key];b.onclick=()=>{mode=key;try{localStorage.setItem('hytale-craft-item-view-v1',mode)}catch{}draw()};bar.append(b)}host.append(bar);draw();return bar}
root.CraftItemVisuals={resolve,category,family,image,modeControl,labels,tiles,extendedTiles,configureResearch,setResearchEnabled,researchEvidence};if(typeof module!=='undefined')module.exports=root.CraftItemVisuals;
})(globalThis);
