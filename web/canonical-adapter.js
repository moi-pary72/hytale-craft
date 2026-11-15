/* Technical correctness and publication rights are separate decisions. No fetching. */
(function(root){'use strict';
function engine(){return root.HytaleCanonicalPlanner||(typeof require==='function'?require('./planner-v2.js'):null)}
function technical(catalog){try{engine().compile(catalog);return {valid:true,errors:[]}}catch(e){return {valid:false,errors:[e.message]}}}
async function publication(catalog,trustedApproval,raw){
 // Approval belongs to reviewed application/build configuration, never to input JSON.
 const supported=trustedApproval?.kind==='original-synthetic'&&trustedApproval.game_data===false&&trustedApproval.source_revision===catalog?.snapshot?.source_revision&&trustedApproval.source_ids?.length===catalog?.sources?.length&&catalog.sources.every(s=>trustedApproval.source_ids.includes(s.id));
 if(!supported||!(raw instanceof ArrayBuffer||ArrayBuffer.isView(raw)))return {allowed:false,reason:'no-trusted-publication-approval'};
 const bytes=raw instanceof ArrayBuffer?new Uint8Array(raw):new Uint8Array(raw.buffer,raw.byteOffset,raw.byteLength);if(bytes.byteLength>1000000)return {allowed:false,reason:'payload-too-large'};
 const cryptoApi=root.crypto||(typeof require==='function'?require('node:crypto').webcrypto:null),digest=[...new Uint8Array(await cryptoApi.subtle.digest('SHA-256',bytes))].map(x=>x.toString(16).padStart(2,'0')).join('');
 let same=false;try{same=JSON.stringify(JSON.parse(new TextDecoder().decode(bytes)))===JSON.stringify(catalog)}catch{}
 return {allowed:digest===trustedApproval.sha256&&same,reason:digest===trustedApproval.sha256&&same?'reviewed-original-learning-data':'payload-mismatch'};
}
function calculate(catalog,goals,inventory,options={}){return engine().compute(catalog,goals,inventory,options)}
function legacy(db,goals,inventory){const planner=root.HytalePlanner||(typeof require==='function'?require('./planner.js'):null);return planner.compute(db,goals,inventory)}
root.CraftCanonical={technical,publication,calculate,legacy};if(typeof module!=='undefined')module.exports=root.CraftCanonical;
})(globalThis);
