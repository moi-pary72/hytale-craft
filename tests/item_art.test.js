const{test}=require('node:test'),a=require('node:assert/strict'),fs=require('fs'),crypto=require('crypto'),v=require('../web/item-visuals.js');
test('four material columns use distinct original tiles without official claims',()=>{const cells=[];for(const material of ['Copper','Iron','Cobalt','Adamantite']){const x=v.resolve({id:'Weapon_Sword_'+material});a.equal(x.level,'interpretation');a.equal(x.official,false);a.equal(x.path,'assets/item-system/materials.webp');cells.push(x.tile)}a.deepEqual(cells,[0,1,2,3])});
test('missing silhouettes are now type-correct original icons',()=>{for(const [id,key]of [['Tool_Shovel_Copper','shovel']]){const x=v.resolve({id});a.equal(x.key,key);a.equal(x.path,'assets/item-system/crafting.webp');a.equal(x.official,false)}});
test('all new atlas files retain their reviewed hashes and byte budgets',()=>{const m=JSON.parse(fs.readFileSync('assets/item-system/manifest.json'));for(const n of ['crafting.webp','materials.webp','weapon-variants.webp']){const raw=fs.readFileSync('assets/item-system/'+n);a.equal(crypto.createHash('sha256').update(raw).digest('hex'),m.files[n].sha256);a.ok(raw.length<200000)}});
test('pickaxe quantities come from the bounded citation, unknown yield is retained',()=>{const i=require('../data/reference-selection.json').items.Tool_Pickaxe_Iron;a.deepEqual(i.recipe.ingredients,{Ingredient_Bar_Iron:5,Ingredient_Leather_Light:2,Ingredient_Fabric_Scrap_Linen:2});a.equal(i.recipe.station,'Workbench');a.equal(i.recipe.output_quantity,null);a.equal(i.build,'0.6.4-b27')});

test('16 new weapon variants have unique verified atlas cells and cover 32 of the public items',()=>{const m=JSON.parse(fs.readFileSync('assets/item-system/manifest.json')),items=require('../data/reference-selection.json').items,seen=new Set();for(const [row,type]of m.weapon_variant_rows.entries())for(const [col,material]of m.weapon_variant_columns.entries()){const id=`Weapon_${type}_${material}`;a.ok(items[id]);const x=v.resolve(items[id]);a.equal(x.level,'interpretation');a.equal(x.path,'assets/item-system/weapon-variants.webp');a.equal(x.tile,row*4+col);a.equal(x.official,false);seen.add(x.tile)}a.equal(seen.size,16);const exact=Object.values(items).map(i=>v.resolve(i)).filter(x=>x.level==='interpretation');a.equal(exact.length,39);a.equal(new Set(exact.map(x=>x.path+'#'+x.tile)).size,39);a.notEqual(v.resolve({id:'Weapon_Mace_Thorium'}).path,'assets/item-system/weapon-variants.webp')});

test('seven additional exact-ID icons extend first weapon batch without overriding it',()=>{const items=require('../data/reference-selection.json').items;const m=JSON.parse(fs.readFileSync('assets/item-system/manifest.json'));for(const [tile,id]of m.weapon_variant_additions.entries()){a.ok(items[id],id);const icon=v.resolve(items[id]);a.equal(icon.level,'interpretation',id);a.equal(icon.path,'assets/item-system/weapon-variants-additions.webp',id);a.equal(icon.tile,tile,id);a.equal(icon.official,false,id)}const data=fs.readFileSync('assets/item-system/weapon-variants-additions.webp');a.equal(crypto.createHash('sha256').update(data).digest('hex'),m.files['weapon-variants-additions.webp'].sha256);a.ok(data.length<200000);a.equal(v.resolve({id:'Weapon_Longsword_Copper'}).path,'assets/item-system/weapon-variants.webp');a.notEqual(v.resolve({id:'Weapon_Spear_Mithril'}).path,'assets/item-system/weapon-variants-additions.webp')});

test('guide card image cap cannot compress an authored sprite atlas into multiple wrong silhouettes',()=>{
 const css=fs.readFileSync('web/item-visuals.css','utf8');
 const four=/\.iv-art\.iv-sprite>img[^{}]*\{([^}]+)\}/.exec(css)?.[1];
 const three=/\.iv-art\.iv-cols3\.iv-sprite>img[^{}]*\{([^}]+)\}/.exec(css)?.[1];
 a.ok(four,'4x4 atlas rule exists');a.ok(three,'3x3 research atlas rule exists');
 for(const [rule,size]of [[four,'400%'],[three,'300%']]){
  for(const part of ['width','height','min-width','min-height'])a.match(rule,new RegExp('(?:^|;)\\s*'+part+':'+size+'(?:;|$)'));
  a.match(rule,/max-height:none/);a.match(rule,/max-width:none/);
 }
 const manifest=JSON.parse(fs.readFileSync('assets/item-system/manifest.json'));
 for(const entry of Object.values(manifest.files))a.equal(entry.width,entry.height,'atlas must be square');
});
test('real ID silhouettes select isolated axe, dagger, mace, spear and shield cells',()=>{
 const cases=[
  ['Weapon_Battleaxe_Iron','battleaxe','materials.webp',5],
  ['Weapon_Daggers_Iron','dagger','weapon-variants.webp',5],
  ['Weapon_Mace_Cobalt','mace','weapon-variants.webp',10],
  ['Weapon_Shield_Adamantite','shield','weapon-variants.webp',15],
  ['Weapon_Spear_Iron','spear','weapon-variants-additions.webp',4],
  ['Weapon_Mace_Thorium','mace','weapon-variants-additions.webp',2]
 ];
 for(const [id,key,asset,tile] of cases){const x=v.resolve({id});a.equal(x.level,'interpretation',id);a.equal(x.key,key,id);a.equal(x.path,'assets/item-system/'+asset,id);a.equal(x.tile,tile,id);a.equal(x.columns,4,id);a.equal(x.official,false,id)}
});
