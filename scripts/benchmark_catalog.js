#!/usr/bin/env node
/* Reproducible ORIGINAL synthetic load test; contains no Hytale facts or network. */
const fs=require('node:fs'),{performance}=require('node:perf_hooks'),p=require('../web/planner-v2.js'),{makeCatalog}=require('../tests/helpers/synthetic-catalog.js');
const elapsed=fn=>{const start=performance.now(),result=fn();return {ms:performance.now()-start,result}},median=values=>values.sort((a,b)=>a-b)[Math.floor(values.length/2)];
const report={kind:'synthetic-only-not-game-data',node:process.version,catalogues:[]};
for(const count of [5000,9999]){
 const data=makeCatalog(count),compiled=elapsed(()=>p.prepare(data)),plan=compiled.result,id=data.items.at(-1).id;
 const cold=[],warm=[],search=[];for(let i=0;i<5;i++){cold.push(elapsed(()=>p.compute(data,{[id]:7})).ms);warm.push(elapsed(()=>plan.compute({[id]:7})).ms);search.push(elapsed(()=>plan.search('Нагрузочный',{offset:100,limit:50})).ms)}
 const goals={},inventory={};for(let i=0;i<500;i++)goals[data.items[i+1].id]=7;for(let i=0;i<3000;i++)inventory[data.items[i+1].id]=1;
 const batch=elapsed(()=>plan.compute(goals,inventory));
 report.catalogues.push({items:plan.stats.items,recipes:count,json_bytes:Buffer.byteLength(JSON.stringify(data)),prepare_ms:compiled.ms,cold_single_goal_median_ms:median(cold),prepared_single_goal_median_ms:median(warm),search_50_median_ms:median(search),batch_500_goals_3000_inventory_ms:batch.ms,batch_trials:batch.result.diagnostics.trials});
 if(process.argv[2]==='--fixture'&&count===5000){fs.mkdirSync('.private/catalog-search',{recursive:true});fs.writeFileSync('.private/catalog-search/generated-5000.json',JSON.stringify(data));}
}
console.log(JSON.stringify(report,null,2));
