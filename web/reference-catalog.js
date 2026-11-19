/* Read-only catalogue index and bounded structural paths. Never assumes batch output. */
(function(root){'use strict';
function prepare(items){
 const table=new Map(Object.entries(items)),text=new Map(),groups=new Map();
 for(const [id,i]of table){text.set(id,(id+' '+Object.values(i.names||{}).filter(Boolean).join(' ')).normalize('NFKC').toLowerCase());const key=i.theme+'|'+i.subcategory;if(!groups.has(key))groups.set(key,[]);groups.get(key).push(id)}
 const methods=id=>{const i=table.get(id);return Array.isArray(i?.methods)?i.methods:i?.recipe?[{id:id+':recipe',...i.recipe}]:[]};
 function status(id){const i=table.get(id);if(!i||i.status==='quarantined')return 'D';const ms=methods(id);if(!ms.length)return 'C';const valid=ms.filter(m=>m.ingredients&&Object.keys(m.ingredients).length&&Object.entries(m.ingredients).every(([k,q])=>k!==id&&table.has(k)&&(q===null||Number.isSafeInteger(q)&&q>0)));if(!valid.length)return 'D';return valid.some(m=>i.verification==='game-verified'&&Number.isSafeInteger(m.output_quantity)&&m.output_quantity>0&&m.station&&Object.values(m.ingredients).every(Number.isSafeInteger))?'A':'B'}
 function search(query='',options={}){const q=query.normalize('NFKC').toLowerCase().trim(),ids=[];for(const [id,i]of table)if((!options.category||i.category===options.category)&&(!options.theme||i.theme===options.theme)&&(!options.subcategory||i.subcategory===options.subcategory)&&(!q||text.get(id).includes(q)))ids.push(id);const lang=options.lang||'en',name=id=>table.get(id).names?.[lang]||table.get(id).names?.en||id;const complexity=id=>methods(id).length?Math.min(...methods(id).map(m=>Object.keys(m.ingredients||{}).length)):Infinity;
 ids.sort((a,b)=>(options.sort==='ingredients'?complexity(a)-complexity(b):options.sort==='progress'?((table.get(a).progression_verified?table.get(a).item_level:Infinity)-(table.get(b).progression_verified?table.get(b).item_level:Infinity)):0)||name(a).localeCompare(name(b),lang));const offset=Math.max(0,options.offset||0),limit=Math.min(48,Math.max(1,options.limit||48));return {total:ids.length,ids:ids.slice(offset,offset+limit)}}
 function path(id,choices={}){let count=0;const build=table.get(id)?.build;
  function walk(key,quantity,active,depth){if(++count>=200||depth>24)return {id:key,status:'limit',children:[]};if(active.has(key))return {id:key,status:'cycle',children:[]};const item=table.get(key);if(!item)return {id:key,status:'unknown',children:[]};if(item.build!==build)return {id:key,status:'version',children:[]};const ms=methods(key),m=ms.find(x=>x.id===choices[key])||ms[0];if(!m)return {id:key,quantity,status:'unknown',children:[]};const next=new Set(active);next.add(key);const children=[];for(const [k,q]of Object.entries(m.ingredients||{})){if(count>=200)break;children.push(walk(k,q,next,depth+1))}return {id:key,quantity,status:'method',method:m.id,methods:ms.map(x=>x.id),station:m.station||null,output_quantity:m.output_quantity??null,local_batch_only:true,children}}
  return walk(id,null,new Set(),0);
 }
 function directMaterials(id,quantity,inventory={},chosenMethod=null){
  if(!Number.isSafeInteger(quantity)||quantity<1||quantity>999999)throw Error('quantity');
  const item=table.get(id);
  // One historical source recipe may be calculated directly. Never infer a current-game recipe.
  if(!item?.recipe||item.recipe.status!=='source-documented-complete')throw Error('unverified');
  if(!inventory||typeof inventory!=='object'||Array.isArray(inventory))throw Error('inventory');
  const available=methods(id),method=chosenMethod===null?available[0]:available.find(m=>m.id===chosenMethod);
  if(!method)throw Error('method');
  const yieldCount=method.output_quantity;
  if(!Number.isSafeInteger(yieldCount)||yieldCount<1)throw Error('yield');
  const batches=Math.ceil(quantity/yieldCount),produced=batches*yieldCount;
  if(!Number.isSafeInteger(produced)||produced>999999999)throw Error('overflow');
  const inputs=Object.entries(method.ingredients||{});
  if(!inputs.length||inputs.length>50)throw Error('ingredients');
  const materials=inputs.map(([key,perCraft])=>{
   // Only first-order ingredients are used, even if their IDs also have recipes in another build.
   if(!table.has(key)||key===id||!Number.isSafeInteger(perCraft)||perCraft<1)throw Error('ingredients');
   const total=perCraft*batches,owned=Object.hasOwn(inventory,key)?inventory[key]:0;
   if(!Number.isSafeInteger(total)||total>999999999||!Number.isSafeInteger(owned)||owned<0||owned>999999)throw Error('overflow');
   return {id:key,perCraft,total,owned,missing:Math.max(0,total-owned)};
  });
  return {kind:'historical-direct-only',build:item.build,method:method.id||null,station:method.station||null,quantity,batches,produced,materials};
 }
 return {search,status,methods,path,directMaterials,groups,items:table};
}
root.CraftReferenceCatalog={prepare};if(typeof module!=='undefined')module.exports=root.CraftReferenceCatalog;
})(globalThis);
