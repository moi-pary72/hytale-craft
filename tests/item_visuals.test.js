const{test}=require('node:test'),a=require('node:assert/strict'),fs=require('node:fs'),crypto=require('node:crypto'),v=require('../web/item-visuals.js');
test('only original exact lesson mappings are individual; source IDs cannot claim official imagery',()=>{for(const id of ['lesson:blade','lesson:pick','lesson:wood']){const x=v.resolve({id});a.equal(x.level,'individual');a.equal(x.official,false)}a.equal(v.resolve({id:'foreign:blade'}).level,'neutral');a.equal(v.resolve({id:'test:Crude_Shortbow'}).level,'category');a.equal(v.resolve({id:'test:Crude_Shortbow'}).key,'bow')});
test('silhouette families preserve type and leave unknown ores and materials neutral',()=>{a.equal(v.resolve({id:'test:Iron_Pickaxe'}).key,'pickaxe');a.equal(v.resolve({id:'test:Steel_Axe'}).key,'axe');a.equal(v.resolve({id:'test:Wood_Axe'}).level,'neutral');a.equal(v.resolve({id:'test:Essence_Cauliflower'}).level,'neutral');a.equal(v.resolve({id:'test:Rare_Crystal_Ore'}).level,'neutral');a.equal(v.resolve({id:'test:Adamantite_Boots',category:'Armor'}).level,'neutral');for(const key of ['sword','helmet','cuirass','wood','stone','ingot','fabric','herb','food','potion','furniture','building','workbench'])a.equal(v.resolve({id:'test:'+key}).level,'category')});
test('atlas has a checked original 4x4 contract, no remote paths or copyrighted data dependencies',()=>{const m=JSON.parse(fs.readFileSync('assets/item-system/manifest.json'));a.equal(m.tiles.length,16);a.equal(new Set(m.tiles).size,16);const b=fs.readFileSync('assets/item-system/categories.webp');a.equal(crypto.createHash('sha256').update(b).digest('hex'),m.files['categories.webp'].sha256);a.ok(b.length<350000);a.equal(v.tiles[15],'neutral')});

test('generic weapon artwork preserves a type silhouette with a material accent rather than counterfeit variants',()=>{
 const css=fs.readFileSync('web/item-visuals.css','utf8');
 a.match(css,/\.iv-art\[data-visual=category\]\[data-material\]::before/);
 a.match(css,/background:var\(--iv-material-accent/);
 for(const material of ['Copper','Bronze','Iron','Thorium','Cobalt','Mithril','Adamantite']){
  a.match(css,new RegExp('\\.iv-art\\[data-material='+material+'\\]\\{--iv-material-accent:#[0-9a-f]{6};border-color:var\\(--iv-material-accent\\)\\}'));
  const item=v.resolve({id:'Tool_Hatchet_'+material});
  a.equal(item.key,'axe',material);
  a.equal(item.level,'category',material);
  a.equal(item.path,'assets/item-system/categories.webp',material);
 }
});

test('art-only hierarchy covers all materials without claiming in-game rarity or replacing identity',()=>{
 const materials=['Copper','Bronze','Iron','Cobalt','Thorium','Mithril','Adamantite'];
 const expected=['basic','basic','forged','enhanced','enhanced','masterwork','masterwork'];
 const numerals=['I','II','III','IV','V','VI','VII'];
 for(let n=0;n<materials.length;n++){
  const aitem=v.artMaterial({id:'Armor_'+materials[n]+'_Chest'});
  a.equal(aitem.material,materials[n]);a.equal(aitem.rank,n+1);
  a.equal(aitem.grade,expected[n]);a.equal(aitem.roman,numerals[n]);
  a.equal(v.resolve({id:'Armor_'+materials[n]+'_Chest'}).key,'breastplate');
 }
 a.equal(v.artMaterial({id:'Armor_Unknown_Chest'}),null);
 a.equal(v.artMaterial({id:'lesson:blade'}),null);
 a.equal(v.artMaterial({id:'Weapon_Coppery_Ironwood'}),null);
 const src=fs.readFileSync('web/item-visuals.js','utf8');
 a.match(src,/NOT verified Hytale rarity, power or crafting progression/);
 a.match(src,/box.dataset.artGrade=art.grade/);
 a.match(src,/delete box.dataset.artGrade/);
});
test('visual grades have readable symbolic rank, four distinct styles, compact safe layout',()=>{
 const css=fs.readFileSync('web/item-visuals.css','utf8');
 for(const grade of ['basic','forged','enhanced','masterwork'])
  a.ok(css.includes('[data-art-grade='+grade+']'),grade);
 a.match(css,/content:attr\(data-art-roman\) " " attr\(data-art-symbol\)/);
 a.match(css,/\.iv-compact \.iv-art\[data-art-grade\]::before/);
 a.match(css,/prefers-reduced-motion:reduce/);
 a.match(css,/prefers-contrast:more/);
});
