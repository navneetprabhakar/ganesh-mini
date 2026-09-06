const {reduceQueue}=require('./solution');const job={id:'a'};Object.defineProperty(job,'id',{enumerable:false});
require('node:assert').strictEqual(reduceQueue(undefined,{type:'ENQUEUE',payload:job}).jobs[0].id,'a');
