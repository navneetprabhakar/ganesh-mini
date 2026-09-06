const {lookupBinSnapshot}=require('./solution');
require('node:assert').rejects(lookupBinSnapshot('x',async()=>({aisle:0,bay:1}),async()=>new Array(1)),TypeError).catch(e=>{throw e;});
