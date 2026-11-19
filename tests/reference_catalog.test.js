const {test}=require('node:test'),a=require('node:assert/strict'),{prepare}=require('../web/reference-catalog.js');
const raw=require('../data/reference-selection.json');
test('real reference paths retain unknown outputs and local batch quantities',()=>{const m=prepare(raw.items),p=m.path('Weapon_Sword_Iron');a.equal(m.status('Weapon_Sword_Iron'),'B');a.equal(p.output_quantity,null);const bar=p.children.find(x=>x.id==='Ingredient_Bar_Iron');a.equal(bar.quantity,6);a.equal(bar.output_quantity,null);a.equal(bar.children[0].id,'Ore_Iron');a.equal(bar.children[0].quantity,1);a.equal(bar.children[0].status,'unknown');a.equal(m.search('Iron Sword',{lang:'ru'}).ids[0],'Weapon_Sword_Iron')});
test('alternatives, cycles and versions do not invent a production chain',()=>{const i={a:{names:{en:'A'},build:'1',methods:[{id:'loop',ingredients:{b:1},output_quantity:null},{id:'safe',ingredients:{c:2},output_quantity:1}]},b:{names:{en:'B'},build:'1',recipe:{ingredients:{a:1}}},c:{names:{en:'C'},build:'2'}};const m=prepare(i);a.equal(m.path('a').children[0].children[0].status,'cycle');a.equal(m.path('a',{a:'safe'}).children[0].status,'version');a.deepEqual(m.path('a').methods,['loop','safe'])});
test('5000 synthetic items have bounded search and paths',()=>{const i={};for(let n=0;n<5000;n++)i['synthetic:'+n]={names:{en:'Synthetic '+n},build:'synthetic',theme:'gather',subcategory:'synthetic',recipe:n?{ingredients:{['synthetic:'+(n-1)]:1},output_quantity:1}:null};const start=performance.now(),m=prepare(i);a.equal(m.search('',{limit:999999}).ids.length,48);a.equal(m.search('synthetic:4999').ids[0],'synthetic:4999');const p=m.path('synthetic:4999');let leaf=p;while(leaf.children.length)leaf=leaf.children[0];a.equal(leaf.status,'limit');a.ok(performance.now()-start<5000)});

test('wide recipes obey the shared 200-node budget',()=>{const ingredients={},items={root:{build:'same',recipe:{ingredients}}};for(let n=0;n<1000;n++){ingredients['child'+n]=1;items['child'+n]={build:'same'}}const p=prepare(items).path('root');a.equal(p.children.length,199);a.equal(p.children.at(-1).status,'limit')});

test('eight individually cited Update 2 recipes have output one, but are not current-game verified',()=>{
 const items=raw.items,ids=['Weapon_Shield_Iron','Weapon_Daggers_Iron','Weapon_Mace_Iron','Weapon_Longsword_Iron','Armor_Iron_Chest','Armor_Iron_Legs','Tool_Hatchet_Iron','Tool_Shovel_Iron'],m=prepare(items);
 a.equal(Object.keys(items).length,100);a.equal(Object.values(items).filter(x=>x.recipe).length,13);
 for(const id of ids){const x=items[id];a.equal(x.source_name,'Hytale Item Laboratory');a.equal(x.recipe.status,'source-documented-complete');a.equal(x.recipe.output_quantity,1);a.equal(m.status(id),'B');const p=m.path(id);a.equal(p.output_quantity,1);a.equal(p.children.length,3);a.ok(p.children.every(c=>c.status==='version'));}
 a.equal(m.methods('Weapon_Mace_Iron').length,2);a.equal(m.path('Weapon_Mace_Iron',{Weapon_Mace_Iron:'forge'}).station,'Forge');a.equal(items.Weapon_Sword_Iron.recipe.output_quantity,null);
});

test('historical direct calculator subtracts owned stock without crossing recipe versions',()=>{
 const model=prepare(raw.items),shield=model.directMaterials('Weapon_Shield_Iron',3,{Ingredient_Bar_Iron:5,Ingredient_Leather_Light:1});
 a.equal(shield.kind,'historical-direct-only');a.equal(shield.batches,3);a.equal(shield.produced,3);
 a.deepEqual(shield.materials.map(x=>[x.id,x.total,x.owned,x.missing]),[
  ['Ingredient_Bar_Iron',12,5,7],['Ingredient_Leather_Light',9,1,8],['Ingredient_Fabric_Scrap_Linen',9,0,9]]);
 a.equal(shield.materials.length,3); // No ore or nested leather recipe from older build.
 const forge=model.directMaterials('Weapon_Mace_Iron',2,{},'forge');
 a.equal(forge.station,'Forge');a.equal(forge.method,'forge');a.equal(forge.materials[0].total,20);
 a.throws(()=>model.directMaterials('Weapon_Mace_Iron',2,{},'nonexistent'),/method/);
 a.throws(()=>model.directMaterials('Weapon_Sword_Iron',3,{}),/unverified/); // Unknown yield: do not guess.
 for(const bad of [0,-1,1.5,NaN,1000000])a.throws(()=>model.directMaterials('Weapon_Shield_Iron',bad,{}),/quantity/);
 a.throws(()=>model.directMaterials('Weapon_Shield_Iron',1,{Ingredient_Bar_Iron:-1}),/overflow/);
});
test('direct quantity uses per-batch output rounding and overflows are refused',()=>{
 const items={product:{build:'history',recipe:{status:'source-documented-complete',output_quantity:3,ingredients:{supply:4},station:'bench'}},supply:{build:'different-build'}};
 const model=prepare(items),estimate=model.directMaterials('product',5,{supply:2});
 a.equal(estimate.batches,2);a.equal(estimate.produced,6);a.equal(estimate.materials[0].missing,6);
 items.product.recipe.ingredients.supply=Number.MAX_SAFE_INTEGER;
 a.throws(()=>model.directMaterials('product',5,{}),/overflow/);
});
