const crypto=require('crypto');
function s(v){if(Array.isArray(v))return v.map(s);if(v&&typeof v==='object'&&v.constructor===Object){return Object.keys(v).sort().reduce((o,k)=>(o[k]=s(v[k]),o),{});}return v;}
function h(v){const c=JSON.stringify(s(v))+'\n';return crypto.createHash('sha256').update(c,'utf8').digest('hex');}
const [l,r]=process.argv.slice(2);
if(!l||!r){console.error('usage: node scripts/merkle-pair-root.js <left> <right>');process.exit(1);} 
console.log(h([l,r]));
