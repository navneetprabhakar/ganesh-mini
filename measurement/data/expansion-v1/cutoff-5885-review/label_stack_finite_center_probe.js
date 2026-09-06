const {placeLabels}=require('./solution');
const m=Number.MAX_VALUE;
const labels=[{text:'a',color:'x',width:0,height:m},{text:'b',color:'x',width:0,height:m}];
const result=placeLabels(0,m,labels);
require('node:assert').strictEqual(result[0].top,-m/2);
