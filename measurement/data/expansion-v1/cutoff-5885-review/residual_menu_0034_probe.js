const { visibleMenu } = require('./solution');
let node = {id:'leaf',roles:['*'],children:[]};
for (let i = 0; i < 10000; i++) node = {id:String(i),roles:['*'],children:[node]};
let result;
try { result = visibleMenu([node], 'admin'); }
catch (error) { throw new Error(`finite acyclic menu depth 10000 failed: ${error.name}`); }
let count = 0;
for (let current = result[0]; current; current = current.children[0]) count++;
if (count !== 10001) throw new Error('menu nodes lost');
