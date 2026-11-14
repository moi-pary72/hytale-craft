(function(root){'use strict';
const supported=['en','ru','es','pt-BR'];
function match(value){const v=String(value||'').toLowerCase();if(v.startsWith('pt'))return'pt-BR';return supported.find(x=>v===x.toLowerCase()||v.startsWith(x.toLowerCase()+'-'))||null}
function detect(saved,languages=[]){return match(saved)||languages.map(match).find(Boolean)||'en'}
function translate(dict,key){if(!Object.hasOwn(dict,key))throw Error('Missing UI translation: '+key);return dict[key]}
root.CraftI18n={supported,match,detect,translate};if(typeof module!=='undefined')module.exports=root.CraftI18n;
})(globalThis);
