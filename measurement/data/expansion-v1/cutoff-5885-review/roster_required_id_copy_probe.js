const {updateRoster}=require('./solution'); const e={id:'x',name:'X',score:0}; Object.defineProperty(e,'id',{enumerable:false}); require('node:assert').strictEqual(updateRoster([e],[])[0].id,'x');
