const trimToBudget=require('./solution');
const m=Number.MAX_VALUE;
const r=trimToBudget([m,m],m);
require('node:assert').deepStrictEqual(r,{start:0,end:1,total:m,removed:[{index:1,weight:m}]});
