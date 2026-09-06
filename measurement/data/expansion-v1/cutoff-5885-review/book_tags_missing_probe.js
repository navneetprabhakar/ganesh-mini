const {normalizeBooks:f}=require('./solution'); require('node:assert').throws(() => f([{isbn:'x',title:'T',tags:new Array(1)}]), TypeError);
