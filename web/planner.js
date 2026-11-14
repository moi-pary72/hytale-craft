/* Shared deterministic calculator. Names/IDs are opaque keys; no game data here. */
(function(root){'use strict';
function compute(db,goals,inventory={}){
 const totals=Object.create(null),steps=Object.create(null),stock=Object.assign(Object.create(null),inventory),stack=new Set();
 function add(obj,k,n){const v=(obj[k]||0)+n;if(!Number.isSafeInteger(v)||v>1e12)throw Error('Quantity overflow');obj[k]=v}
 let calls=0;
 function walk(k,n,depth){
  if(++calls>20000)throw Error("Calculation limit exceeded");
  if(depth>100)throw Error('Recipe chain too deep');
  if(!Number.isSafeInteger(n)||n<1||n>1e12)throw Error('Invalid quantity');
  const used=Math.min(stock[k]||0,n);stock[k]=(stock[k]||0)-used;n-=used;if(!n)return;
  if(stack.has(k))throw Error('Recipe cycle: '+[...stack,k].join(' → '));
  if(!Object.hasOwn(db,k)){add(totals,k,n);return}
  const r=db[k];if(!Number.isSafeInteger(r.yield)||r.yield<1)throw Error('Invalid recipe yield');
  stack.add(k);const batches=Math.ceil(n/r.yield);add(steps,k,batches);
  // Surplus becomes available only after its ingredients have been produced.
  for(const [id,q] of Object.entries(r.ingredients)){if(!Number.isSafeInteger(q)||q<1)throw Error('Invalid ingredient');walk(id,batches*q,depth+1)}
  add(stock,k,batches*r.yield-n);stack.delete(k);
 }
 for(const [k,n] of Object.entries(goals))walk(k,n,0);
 return {totals,steps,stock};
}
root.HytalePlanner={compute};if(typeof module!=='undefined')module.exports=root.HytalePlanner;
})(globalThis);
