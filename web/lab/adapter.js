/* Local research adapter. Technical validity never grants publication rights. */
(function(root){'use strict';
function prepare(bundle){
 if(bundle?.policy?.local_only!==true||bundle.policy.public_distribution!==false)throw Error('Research boundary missing');
 const core=root.HytaleCanonicalPlanner||(typeof require==='function'?require('../planner-v2.js'):null),data=bundle.canonical,planner=core.prepare(data);
 const items=new Map(data.items.map(i=>[i.id,i])),recipes=new Map(data.recipes.map(r=>[r.id,r])),producers=new Map(),used=new Map(),blocked=new Set(bundle.meta.blocked_items||[]);
 for(const r of data.recipes){for(const out of r.outputs){if(!producers.has(out.item_id))producers.set(out.item_id,[]);producers.get(out.item_id).push(r)}for(const term of r.inputs)for(const o of term.options)if(o.kind==='item'){if(!used.has(o.id))used.set(o.id,new Set());for(const out of r.outputs)used.get(o.id).add(out.item_id)}}
 function compute(goals,inventory={},options={}){const value=planner.compute(goals,inventory,options),unresolved=Object.keys(value.totals).filter(id=>blocked.has(id));return {...value,unresolved,complete:!unresolved.length,materialOnly:!options.strictRequirements,externalItems:[...(options.externalItems||[])]}}
 function availability(id,inventory={},options={}){
  if(!producers.has(id))return {id,status:blocked.has(id)?'incomplete':'no-method',maximum:0};
  const own=inventory[id]||0,stock=Object.assign(Object.create(null),inventory);delete stock[id];
  function trial(q){return compute({[id]:q},stock,options)}
  try{const first=trial(1);if(!first.complete)return {id,status:'incomplete',maximum:0,result:first};if(Object.values(first.totals).some(q=>q>0))return {id,status:'missing',maximum:0,result:first};
   let low=1,high=2;const cap=999999;while(high<=cap){const x=trial(high);if(!x.complete||Object.values(x.totals).some(q=>q>0))break;low=high;high*=2}high=Math.min(high,cap+1);while(low+1<high){const m=Math.floor((low+high)/2),v=trial(m);if(v.complete&&!Object.values(v.totals).some(q=>q>0))low=m;else high=m}
   const goalRecipe=(producers.get(id)||[]).find(r=>Object.hasOwn(first.steps,r.id)),direct=goalRecipe&&goalRecipe.inputs.every(s=>s.options.some(o=>o.kind==='item'&&(stock[o.id]||0)>=s.quantity));first.stock[id]=(first.stock[id]||0)+own;
   return {id,status:direct?'direct':'chain',maximum:low,capped:low===cap,result:first};
  }catch(e){return {id,status:e.message==='canonicalCycle'?'cycle':e.message==='canonicalRequirements'?'requirements':'unsupported',maximum:0,error:e.message}}
 }
 function path(id,q=1,choices={},externalItems=[]){let nodes=0;const external=new Set(externalItems);
  function walk(id,q,depth,active){if(++nodes>500||depth>60)throw Error('canonicalLimit');if(external.has(id))return {id,quantity:q,raw:true,external:true,children:[]};if(active.has(id))throw Error('canonicalCycle');
   const methods=producers.get(id)||[],r=methods.find(r=>r.id===choices[id])||methods[0];if(!r)return {id,quantity:q,raw:true,incomplete:blocked.has(id),children:[]};
   const next=new Set(active);next.add(id);const output=r.outputs.find(o=>o.item_id===id),batches=Math.ceil(q/output.quantity);
   return {id,quantity:q,recipe:r.id,batches,alternativeCount:methods.length,children:r.inputs.map(s=>{if(s.options.length!==1||s.options[0].kind!=='item')return {id:'unresolved selector',quantity:s.quantity*batches,incomplete:true,children:[]};return walk(s.options[0].id,s.quantity*batches,depth+1,next)})};
  }return walk(id,q,0,new Set());
 }
 const cycleInputs=[...new Set((bundle.meta.validation_warnings||[]).flatMap(w=>(w.paths||[]).flat()))].filter(id=>items.has(id));

 return {data,meta:bundle.meta,items,recipes,producers,blocked,cycleInputs,search:planner.search,stats:planner.stats,compute,availability,path,usedIn:id=>[...(used.get(id)||[])]};
}
root.CraftLab={prepare};if(typeof module!=='undefined')module.exports=root.CraftLab;
})(globalThis);
