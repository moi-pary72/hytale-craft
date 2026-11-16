/* Inventory discovery delegates every calculation to the existing planner. No storage/network. */
(function(root){'use strict';
const units=(map,id)=>Object.hasOwn(map,id)?map[id]:0;
const engine=()=>root.HytalePlanner||(typeof require==='function'?require('./planner.js'):null);
function prepare(db){
 if(!db||typeof db!=='object'||Array.isArray(db)||Object.keys(db).length>10000)throw Error('limit');
 const ids=Object.keys(db),used=new Map();
 for(const [id,r] of Object.entries(db)){
  if(!r||!Number.isSafeInteger(r.yield)||r.yield<1||r.yield>999999||!r.ingredients||!Object.keys(r.ingredients).length)throw Error('recipeError');
  for(const [key,q] of Object.entries(r.ingredients)){if(!Number.isSafeInteger(q)||q<1||q>999999)throw Error('recipeError');if(!used.has(key))used.set(key,[]);used.get(key).push(id)}
 }
 function evaluate(id,inventory,quantity=1){
  if(!Object.hasOwn(db,id))throw Error('recipeError');
  const copy=Object.assign(Object.create(null),inventory),owned=copy[id]||0;delete copy[id];
  const result=engine().compute(db,{[id]:quantity},copy);result.stock[id]=(result.stock[id]||0)+owned;
  return {...result,available:Object.values(result.totals).every(q=>q===0),direct:Object.entries(db[id].ingredients).every(([key,q])=>units(inventory,key)>=q*Math.ceil(quantity/db[id].yield))};
 }
 function capacity(id,inventory){
  const first=evaluate(id,inventory);if(!first.available)return {id,status:'missing',maximum:0,result:first};
  const yieldSize=db[id].yield,cap=Math.floor(999999/yieldSize);let low=1,high=2;
  while(high<=cap&&evaluate(id,inventory,high*yieldSize).available){low=high;high*=2}
  high=Math.min(high,cap+1);while(low+1<high){const mid=Math.floor((low+high)/2);if(evaluate(id,inventory,mid*yieldSize).available)low=mid;else high=mid}
  return {id,status:first.direct?'direct':'chain',maximum:low*yieldSize,capped:low===cap,result:first};
 }
 function together(selected,inventory){
  const goals=Object.create(null);for(const [id,q] of Object.entries(selected)){if(!Object.hasOwn(db,id)||!Number.isSafeInteger(q)||q<1||q>999999)throw Error('badQuantity');goals[id]=q+units(inventory,id)}
  if(!Object.keys(goals).length)throw Error('noGoals');
  const result=engine().compute(db,goals,inventory);
  // The original target stock is reserved, so selected quantities mean additional items.
  for(const id of Object.keys(goals))result.stock[id]=(result.stock[id]||0)+units(inventory,id);
  return {...result,available:!Object.values(result.totals).some(q=>q>0)};
 }
 return Object.freeze({ids:Object.freeze(ids),usedIn:id=>[...(used.get(id)||[])],evaluate,capacity,together});
}
root.Craftable={prepare};if(typeof module!=='undefined')module.exports=root.Craftable;
})(globalThis);
