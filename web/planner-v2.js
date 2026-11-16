/* Original canonical-v2 planner. Pure local computation; no network or storage. */
(function(root){'use strict';
const compare=(a,b)=>a<b?-1:a>b?1:0;
const own=(v,k)=>v&&Object.hasOwn(v,k)?v[k]:undefined;
const MAX=1e12,fail=code=>{throw Error(code)},obj=v=>v&&typeof v==='object'&&!Array.isArray(v),integer=(v,min=1,max=999999)=>Number.isSafeInteger(v)&&v>=min&&v<=max;
function compile(input){
 let data;try{data=JSON.parse(JSON.stringify(input,(_k,v)=>{if(typeof v==='number'&&!Number.isFinite(v))fail('canonicalInvalid');return v}))}catch{fail('canonicalInvalid')}
 const check=(ok)=>{if(!ok)fail('canonicalInvalid')},id=v=>typeof v==='string'&&/^[A-Za-z0-9_.:-]{1,200}$/.test(v),list=(v,max)=>Array.isArray(v)&&v.length<=max;
 check(obj(data)&&data.schema_version===2&&obj(data.snapshot));for(const k of ['game_version','channel','source_revision','updated_at'])check(typeof data.snapshot[k]==='string'&&data.snapshot[k].length>0&&data.snapshot[k].length<=500);
 const exact=(value,keys)=>obj(value)&&Object.keys(value).length===keys.length&&keys.every(k=>Object.hasOwn(value,k));
 const tables={};for(const section of ['sources','items','groups','stations','recipes']){check(list(data[section],10000));const map=new Map();for(const r of data[section]){check(obj(r)&&id(r.id)&&!map.has(r.id));map.set(r.id,r)}tables[section]=map}
 check(tables.items.size>0&&tables.sources.size>0&&tables.recipes.size>0);
 for(const section of ['items','groups','stations','recipes'])for(const r of tables[section].values()){check(tables.sources.has(r.source_id)&&typeof r.source_record==='string'&&r.source_record.length>0&&['verified','unverified','tutorial','incomplete','blocked'].includes(r.status));check((r.game_version??data.snapshot.game_version)===data.snapshot.game_version&&(r.channel??data.snapshot.channel)===data.snapshot.channel)}
 for(const g of tables.groups.values()){check(['resource_type','item_tag','explicit'].includes(g.kind)&&['mixed','single','unknown'].includes(g.selection)&&typeof g.membership_complete==='boolean'&&list(g.members,5000)&&(!g.membership_complete||g.members.length>0));const seen=new Set();for(const m of g.members){check(obj(m)&&tables.items.has(m.item_id)&&integer(m.units)&&!seen.has(m.item_id));seen.add(m.item_id)}}
 const producers=new Map();for(const r of tables.recipes.values()){
  check(['craft','processing','salvage','unknown'].includes(r.kind)&&list(r.inputs,100)&&r.inputs.length&&list(r.outputs,100)&&r.outputs.length);
  for(const s of r.inputs){check(exact(s,['quantity','options'])&&integer(s.quantity)&&list(s.options,50)&&s.options.length);const seen=new Set();for(const o of s.options){check(exact(o,['kind','id'])&&['item','group'].includes(o.kind)&&(o.kind==='item'?tables.items:tables.groups).has(o.id)&&!seen.has(o.kind+'|'+o.id));seen.add(o.kind+'|'+o.id)}}
  const outputs=new Set();for(const o of r.outputs){check(exact(o,['item_id','quantity'])&&tables.items.has(o.item_id)&&integer(o.quantity)&&!outputs.has(o.item_id));outputs.add(o.item_id);if(!producers.has(o.item_id))producers.set(o.item_id,[]);producers.get(o.item_id).push(r)}check(r.primary_output===null||outputs.has(r.primary_output));
  const b=r.station_requirements;check(exact(b,['mode','entries'])&&['any','all','unknown'].includes(b.mode)&&list(b.entries,50));for(const e of b.entries){check(exact(e,['station_id','type','min_level','categories','augment_tags'])&&tables.stations.has(e.station_id)&&['Crafting','Processing','DiagramCrafting','StructuralCrafting','unknown'].includes(e.type)&&(e.min_level===null||integer(e.min_level,0)));for(const k of ['categories','augment_tags'])check(list(e[k],50)&&e[k].every(v=>typeof v==='string'&&v.length>0&&v.length<=500))}
  check(exact(r.requirements,['knowledge_required','memories_level'])&&(r.requirements.knowledge_required===null||typeof r.requirements.knowledge_required==='boolean')&&(r.requirements.memories_level===null||integer(r.requirements.memories_level))&&(r.time_seconds==null||typeof r.time_seconds==='number'&&Number.isFinite(r.time_seconds)&&r.time_seconds>=0&&r.time_seconds<=999999));
 }
 return {data,tables,producers};
}
function requirements(recipe,options){
 const available=options.stations,known=options.knownRecipes;
 function station(e){const v=available&&Object.hasOwn(available,e.station_id)?available[e.station_id]:undefined;if(v===undefined)return available?'missing':'unknown';const actual=typeof v==='number'?{level:v}:v;if(!obj(actual)||!integer(actual.level,0,MAX))fail('canonicalOptions');let unknown=e.min_level===null||e.type==='unknown'||actual.type===undefined;if(e.min_level!==null&&actual.level<e.min_level)return 'missing';if(actual.type!==undefined&&actual.type!==e.type)return 'missing';for(const [required,provided] of [['categories','categories'],['augment_tags','augment_tags']])if(e[required].length){if(!Array.isArray(actual[provided]))unknown=true;else if(!e[required].every(x=>actual[provided].includes(x)))return 'missing'}return unknown?'unknown':'available'}
 const entries=recipe.station_requirements.entries.map(e=>({...e,categories:[...e.categories],augment_tags:[...e.augment_tags],status:station(e)})),mode=recipe.station_requirements.mode;
 let status=mode==='unknown'?'unknown':!entries.length?'available':mode==='any'?(entries.some(e=>e.status==='available')?'available':entries.some(e=>e.status==='unknown')?'unknown':'missing'):(entries.some(e=>e.status==='missing')?'missing':entries.some(e=>e.status==='unknown')?'unknown':'available');
 const k=recipe.requirements.knowledge_required,m=recipe.requirements.memories_level;let unlock=k===null||m===null?'unknown':'available';if(k===true){if(!known)unlock='unknown';else if(!known.includes(recipe.id))unlock='missing'}if(m!==null){if(options.memoriesLevel===undefined){if(unlock!=='missing')unlock='unknown'}else if(options.memoriesLevel<m)unlock='missing'}
 return {recipe_id:recipe.id,mode,entries,station_status:status,unlock_status:unlock,requirements:{...recipe.requirements}};
}
function run(model,goals,inventory={},options={}){
 const {tables,producers}=model;
 if(!obj(goals)||!obj(inventory)||!obj(options)||Object.keys(goals).length>500||Object.keys(inventory).length>10000)fail('canonicalOptions');
 if(options.externalItems!==undefined&&(!Array.isArray(options.externalItems)||options.externalItems.length>10000||options.externalItems.some(id=>typeof id!=='string'||!tables.items.has(id))))fail('canonicalOptions');const external=new Set(options.externalItems||[]);
 for(const k of ['allowSalvage','strictRequirements'])if(options[k]!==undefined&&typeof options[k]!=='boolean')fail('canonicalOptions');
 if(options.knownRecipes!==undefined&&(!Array.isArray(options.knownRecipes)||options.knownRecipes.length>10000||options.knownRecipes.some(x=>typeof x!=='string')))fail('canonicalOptions');if(options.memoriesLevel!==undefined&&!integer(options.memoriesLevel,1,MAX))fail('canonicalOptions');if(options.stations!==undefined&&!obj(options.stations))fail('canonicalOptions');for(const k of ['recipeChoices','materialChoices'])if(options[k]!==undefined&&!obj(options[k]))fail('canonicalOptions');
 let state={stock:Object.assign(Object.create(null),inventory),totals:Object.create(null),steps:Object.create(null),requirements:Object.create(null),waste:Object.create(null),consumed:Object.create(null)},calls=0,trials=0;
 for(const [id,n] of Object.entries(inventory))if(!integer(n,0,MAX))fail('canonicalQuantity');for(const [id,n] of Object.entries(goals))if(!tables.items.has(id)||!integer(n,1,MAX))fail('canonicalQuantity');
 const add=(map,id,n)=>{if(!integer(n,0,MAX)||!integer((map[id]||0)+n,0,MAX))fail('canonicalLimit');map[id]=(map[id]||0)+n},times=(a,b)=>{const n=a*b;if(!integer(n,0,MAX))fail('canonicalLimit');return n},clone=s=>({stock:Object.assign(Object.create(null),s.stock),totals:Object.assign(Object.create(null),s.totals),steps:Object.assign(Object.create(null),s.steps),requirements:Object.assign(Object.create(null),s.requirements),waste:Object.assign(Object.create(null),s.waste),consumed:Object.assign(Object.create(null),s.consumed)});
 function use(s,id,n,asInput=false){const used=Math.min(s.stock[id]||0,n);s.stock[id]=(s.stock[id]||0)-used;if(asInput)add(s.consumed,id,used);return n-used}
 function score(s){return [Object.values(s.totals).reduce((a,b)=>a+BigInt(b),0n),Object.values(s.steps).reduce((a,b)=>a+BigInt(b),0n),Object.values(s.waste).reduce((a,b)=>a+BigInt(b),0n)]}
 function better(a,b){const x=score(a),y=score(b);for(let i=0;i<x.length;i++)if(x[i]!==y[i])return x[i]<y[i];return false}
 function choose(s,actions){let best,error;for(const action of actions){if(++trials>2000)fail('canonicalLimit');try{const next=action(clone(s));if(!best||better(next,best))best=next}catch(e){if(e.message==='canonicalLimit')throw e;error=e}}if(!best)throw error||Error('canonicalNoRoute');return best}
 function group(s,g,q,stack,depth,forced){if(!g.membership_complete||g.selection==='unknown')fail('canonicalGroup');let members=g.members.slice().sort((a,b)=>b.units-a.units||compare(a.item_id,b.item_id));if(forced){members=members.filter(m=>m.item_id===forced);if(!members.length)fail('canonicalChoice')}
  const finish=(start,remaining,list)=>choose(start,list.map(m=>t=>{const count=Math.ceil(remaining/m.units),next=walk(t,m.item_id,count,stack,depth);add(next.waste,g.id,count*m.units-remaining);return next}));
  if(g.selection==='single'||forced)return finish(s,q,members);
  let remaining=q;for(const m of members){const count=Math.min(s.stock[m.item_id]||0,Math.floor(remaining/m.units));if(count){use(s,m.item_id,count,true);remaining-=count*m.units}if(!remaining)return s}
  return finish(s,remaining,members);
 }
 function slot(s,r,index,batches,stack,depth){const term=r.inputs[index],q=times(term.quantity,batches),forced=own(own(options.materialChoices,r.id),index);if(forced!==undefined&&typeof forced!=='string')fail('canonicalChoice');const actions=[];
  for(const o of term.options){if(o.kind==='item'){if(!forced||forced===o.id)actions.push(t=>walk(t,o.id,q,stack,depth))}else{const g=tables.groups.get(o.id);if(!forced||g.members.some(m=>m.item_id===forced))actions.push(t=>group(t,g,q,stack,depth,forced))}}
  if(!actions.length)fail('canonicalChoice');return choose(s,actions);
 }
 function walk(s,id,n,stack,depth){if(++calls>20000||depth>100)fail('canonicalLimit');n=use(s,id,n,depth>0);if(!n)return s;if(external.has(id)){add(s.totals,id,n);if(depth>0)add(s.consumed,id,n);return s}if(stack.includes(id))fail('canonicalCycle');
  const explicit=own(options.recipeChoices,id);if(explicit!==undefined&&typeof explicit!=='string')fail('canonicalChoice');const allRecipes=producers.get(id)||[];if(allRecipes.length&&allRecipes.every(r=>r.kind==='unknown'))fail('canonicalIncomplete');let recipes=allRecipes.filter(r=>r.kind!=='unknown');if(explicit){recipes=recipes.filter(r=>r.id===explicit);if(!recipes.length)fail('canonicalChoice');if(recipes[0].kind==='salvage'&&!options.allowSalvage)fail('canonicalSalvage')}else recipes=recipes.filter(r=>r.kind!=='salvage'||options.allowSalvage);
  if(!recipes.length){add(s.totals,id,n);if(depth>0)add(s.consumed,id,n);return s}
  const ancestry=[...stack,id];recipes.sort((a,b)=>compare(a.id,b.id));return choose(s,recipes.map(r=>t=>{if(['blocked','incomplete'].includes(r.status))fail('canonicalIncomplete');const checks=requirements(r,options);if(options.strictRequirements&&(checks.station_status!=='available'||checks.unlock_status!=='available'))fail('canonicalRequirements');const out=r.outputs.find(o=>o.item_id===id),batches=Math.ceil(n/out.quantity);for(let i=0;i<r.inputs.length;i++)t=slot(t,r,i,batches,ancestry,depth+1);for(const o of r.outputs)add(t.stock,o.item_id,times(o.quantity,batches));if(use(t,id,n,depth>0))fail('canonicalNoRoute');add(t.steps,r.id,batches);t.requirements[r.id]=checks;return t}));
 }
 // Co-producing requested outputs first avoids purchasing a goal supplied as a by-product.
 const targets=Object.entries(goals),goalIds=new Set(targets.map(([id])=>id));function coScore(id){return Math.max(0,...(producers.get(id)||[]).filter(r=>r.kind!=='salvage'||options.allowSalvage).map(r=>r.outputs.filter(o=>goalIds.has(o.item_id)).length))}targets.sort((a,b)=>coScore(b[0])-coScore(a[0]));
 for(const [id,n] of targets)state=walk(state,id,n,[],0);
 return {...state,requirements:Object.values(state.requirements),strategy:'bounded-stock-first',optimal:false,diagnostics:{calls,trials}};
}
function compute(input,goals,inventory={},options={}){return run(compile(input),goals,inventory,options)}
function prepare(input){
 // Private validated snapshot: never accept a caller-supplied compiled model.
 const model=compile(input),{tables,producers}=model;
 const normalize=value=>value.normalize('NFKC').toLowerCase();
 const index=[...tables.items.values()].map(item=>{
  const names=Object.fromEntries(Object.entries(obj(item.names)?item.names:{}).filter(([k,v])=>['en','ru','es','pt-BR'].includes(k)&&typeof v==='string'));
  const category=typeof item.category==='string'?item.category:'';
  const recipes=producers.get(item.id)||[];
  return {id:item.id,names,category,recipes,text:normalize([item.id,category,...Object.values(names)].join(' '))};
 }).sort((a,b)=>compare(a.id,b.id));
 function search(query='',filters={}){
  if(typeof query!=='string'||query.length>200||!obj(filters))fail('canonicalOptions');
  const {offset=0,limit=50,category,station,kind,catalogLimit=10000}=filters;
  if(!integer(catalogLimit,1,10000)||!integer(offset,0,10000)||!integer(limit,1,100)||[category,station,kind].some(v=>v!==undefined&&typeof v!=='string')||(kind!==undefined&&!['craft','processing','salvage','unknown'].includes(kind)))fail('canonicalOptions');
  const tokens=normalize(query).trim().split(/\s+/).filter(Boolean),items=[];let total=0;
  for(const row of catalogLimit===10000?index:index.slice(0,catalogLimit)){if(!tokens.every(t=>row.text.includes(t))||(category!==undefined&&row.category!==category))continue;
   const recipes=row.recipes.filter(r=>(kind===undefined||r.kind===kind)&&(station===undefined||r.station_requirements.entries.some(e=>e.station_id===station)));
   if((kind!==undefined||station!==undefined)&&!recipes.length)continue;
   if(total>=offset&&items.length<limit)items.push({id:row.id,names:{...row.names},category:row.category,recipe_ids:recipes.map(r=>r.id)});
   total++;
  }
  return {total,offset,limit,items};
 }
 return Object.freeze({compute:(goals,inventory={},options={})=>run(model,goals,inventory,options),search,stats:Object.freeze({items:tables.items.size,recipes:tables.recipes.size,groups:tables.groups.size,stations:tables.stations.size})});
}
const api={compile,compute,prepare,requirements};root.HytaleCanonicalPlanner=api;if(typeof module!=='undefined')module.exports=api;
})(globalThis);
