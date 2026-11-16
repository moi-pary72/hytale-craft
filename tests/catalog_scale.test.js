const {test}=require('node:test'),assert=require('node:assert/strict'),p=require('../web/planner-v2.js'),{makeCatalog}=require('./helpers/synthetic-catalog.js');
test('prepared 5000-recipe snapshot supports 500 goals and a large shared inventory',()=>{
 const d=makeCatalog(),plan=p.prepare(d),goals={},inventory={};let required=0;
 for(let i=0;i<500;i++){const id=d.items[i+1].id;goals[id]=7;inventory[id]=1;required+=Math.ceil(6/(i%3+1))*(i%5+1)}
 for(let i=500;i<3000;i++)inventory[d.items[i+1].id]=1;
 const x=plan.compute(goals,inventory);assert.equal(x.totals['load:raw'],required);assert.equal(Object.keys(x.steps).length,500);assert.equal(inventory[d.items[1].id],1);assert.equal(plan.stats.recipes,5000);assert.deepEqual(x,plan.compute(goals,inventory));
});
test('prepared snapshot is isolated from input edits and returned search/result mutations',()=>{
 const d=makeCatalog(20),plan=p.prepare(d),id=d.items[1].id,expected=plan.compute({[id]:2});d.recipes[0].inputs[0].quantity=99;d.items[1].names.en='Changed';
 const rows=plan.search('load:item-00000');rows.items[0].names.en='Tampered';rows.items[0].recipe_ids.push('absent');const pristine=JSON.stringify(expected);expected.stock[id]=99;for(const r of expected.requirements)for(const e of r.entries){e.categories.push('tampered');e.augment_tags.push('tampered')}assert.equal(JSON.stringify(plan.compute({[id]:2})),pristine);
 assert.equal(plan.search('load:item-00000').items[0].names.en,'Load item 0');assert.equal(plan.search('load:item-00000').items[0].recipe_ids.length,1);assert.equal(plan.compute({[id]:2}).totals['load:raw'],2);assert.equal(plan.compute({[id]:2}).stock[id],0);assert.equal(Object.isFrozen(plan),true);
});
test('catalogue search is bounded, multilingual and filters recipes without losing raw items',()=>{
 const plan=p.prepare(makeCatalog());assert.equal(plan.search().total,5001);assert.equal(plan.search().items.length,50);assert.equal(plan.search('НАГРУЗОЧНЫЙ 4999').items[0].id,'load:item-04999');assert.equal(plan.search('Objeto carga 4999').total,1);assert.equal(plan.search('Item de carga 4999').total,1);assert.equal(plan.search('Load item 4999').total,1);assert.equal(plan.search('',{category:'odd'}).total,2500);assert.equal(plan.search('',{kind:'salvage'}).total,0);assert.equal(plan.search('',{station:'sample:station'}).total,5000);
 const a=plan.search('',{offset:50,limit:50}),b=plan.search('',{offset:100,limit:50});assert.equal(a.items.length,50);assert.equal(new Set([...a.items,...b.items].map(r=>r.id)).size,100);assert.equal(plan.search('load:raw').items[0].recipe_ids.length,0);
 for(const f of [{limit:1000},{offset:-1},{kind:'made-up'},null])assert.throws(()=>plan.search('',f),/canonicalOptions/);
 assert.throws(()=>plan.search('x'.repeat(201)),/canonicalOptions/);
});
test('10000-table boundaries stay explicit and technical preparation grants no publication rights',async()=>{
 assert.equal(p.prepare(makeCatalog(9999)).stats.items,10000);assert.throws(()=>p.prepare(makeCatalog(10000)),/canonicalInvalid/);
 const adapter=require('../web/canonical-adapter.js'),d=makeCatalog(10);assert.equal(adapter.prepare(d).stats.recipes,10);assert.equal((await adapter.publication(d)).allowed,false);
});
test('catalogue sample limits keep full dependency snapshot and independent pagination',()=>{const plan=p.prepare(makeCatalog(1000));assert.equal(plan.search('',{catalogLimit:100}).total,100);assert.equal(plan.search('',{catalogLimit:1000,limit:24}).total,1000);assert.equal(plan.search('',{catalogLimit:1000,offset:24,limit:24}).items.length,24);assert.throws(()=>plan.search('',{catalogLimit:0}),/canonicalOptions/);assert.throws(()=>plan.search('',{catalogLimit:10001}),/canonicalOptions/);assert.equal(plan.stats.items,1001)});
