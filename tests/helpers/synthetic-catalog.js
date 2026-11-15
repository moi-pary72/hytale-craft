/* Original generated benchmark records, not game facts. Never a public catalogue. */
const base=require('../fixtures/catalog-v2-synthetic.json');
function makeCatalog(count=5000){
 const data=structuredClone(base),item=structuredClone(data.items[0]),recipe=structuredClone(data.recipes[0]);
 data.items=[{...item,id:'load:raw',source_record:'generated/raw',names:{en:'Original load-test material'},category:'load-only'}];data.groups=[];data.recipes=[];
 for(let i=0;i<count;i++){
  const id='load:item-'+String(i).padStart(5,'0');
  data.items.push({...item,id,source_record:'generated/'+i,names:{en:'Load item '+i,ru:'Нагрузочный предмет '+i,es:'Objeto de carga '+i,'pt-BR':'Item de carga '+i},category:i%2?'odd':'even'});
  data.recipes.push({...structuredClone(recipe),id:'load:recipe-'+i,source_record:'generated/recipe/'+i,inputs:[{quantity:i%5+1,options:[{kind:'item',id:'load:raw'}]}],outputs:[{item_id:id,quantity:i%3+1}],primary_output:id});
 }
 return data;
}
module.exports={makeCatalog};
