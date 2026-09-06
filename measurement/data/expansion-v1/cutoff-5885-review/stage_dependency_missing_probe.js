const {orderStages}=require('./solution'); require('node:assert').throws(() => orderStages([{name:'a',after:new Array(1)}]),TypeError);
