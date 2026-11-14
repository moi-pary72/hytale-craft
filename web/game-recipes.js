/* Version-isolated adapter. Never joins third-party snapshots or local user recipes. */
(function(root){'use strict';
function validate(data){
 if(data?.schema_version!==3||typeof data.source?.extracted_at!=='string'||!data.source.extracted_at||!Array.isArray(data.items)||!Array.isArray(data.recipes)||!data.recipes.length)throw Error('Invalid recipe snapshot');
 const known=new Set();for(const i of data.items){if(!i||typeof i.id!=='string'||!i.id||known.has(i.id)||i.names&&Object.values(i.names).some(n=>n!==null&&typeof n!=='string'))throw Error('Duplicate item ID');known.add(i.id)}
 const seen=new Set();for(const r of data.recipes){
  if(typeof r.id!=='string'||seen.has(r.id)||r.status!=='source-backed'||!Array.isArray(r.inputs)||!r.inputs.length||!Array.isArray(r.outputs)||r.outputs.length!==1||!Array.isArray(r.bench_requirements))throw Error('Unsupported recipe');seen.add(r.id);
  for(const b of r.bench_requirements)if(!b||typeof b.id!=='string'||!b.id||(b.tier!=null&&(!Number.isSafeInteger(b.tier)||b.tier<0)))throw Error('Invalid station');
  for(const m of [...r.inputs,...r.outputs])if(!m||m.kind!=='ItemId'||!known.has(m.id)||!Number.isSafeInteger(m.quantity)||m.quantity<1||m.quantity>999999)throw Error('Unresolved recipe material');
 }
 if(data.incomplete_recipes!==undefined&&(!Array.isArray(data.incomplete_recipes)||data.incomplete_recipes.some(r=>!r||!Array.isArray(r.outputs)||r.outputs.some(id=>typeof id!=='string')||!Array.isArray(r.reasons)||r.reasons.some(x=>typeof x!=='string'))))throw Error('Invalid incomplete records');
 return data;
}
function index(data){validate(data);const byOutput=Object.create(null);for(const r of data.recipes){const id=r.outputs[0].id;(byOutput[id]??=[]).push(r)}return byOutput}
function plan(data,goals,inventory={},choices={},acquire={}){
 const byOutput=index(data),db=Object.create(null),used=Object.create(null),seen=new Set();
 function visit(id){if(acquire[id]&&!Object.hasOwn(goals,id))return;if(seen.has(id))return;seen.add(id);const variants=byOutput[id];if(!variants)return;
  const recipe=variants.find(r=>r.id===choices[id])||(variants.length===1?variants[0]:null);
  if(!recipe)throw Error('Choose recipe: '+id);
  const ingredients=Object.create(null);for(const m of recipe.inputs)ingredients[m.id]=(ingredients[m.id]||0)+m.quantity;
  db[id]={yield:recipe.outputs[0].quantity,ingredients};used[id]=recipe;
  for(const m of recipe.inputs)visit(m.id);
 }
 for(const id of Object.keys(goals)){if(!byOutput[id])throw Error('No confirmed recipe: '+id);visit(id)}
 const result=root.HytalePlanner.compute(db,goals,inventory),stations=[];
 for(const id of Object.keys(result.steps))for(const bench of used[id].bench_requirements){const text=JSON.stringify(bench);if(!stations.some(x=>JSON.stringify(x)===text))stations.push(bench)}
 const incomplete=new Set((data.incomplete_recipes||[]).filter(r=>!r.reasons?.includes('salvage_not_auto_crafted')).flatMap(r=>r.outputs||[]));
 return {...result,stations,unexpanded:Object.keys(result.totals).filter(id=>incomplete.has(id)),recipes:used};
}
root.HytaleGame={validate,index,plan};if(typeof module!=='undefined')module.exports=root.HytaleGame;
})(globalThis);
