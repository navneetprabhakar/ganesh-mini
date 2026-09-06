const {encodeFacetPath:f}=require('./solution'); require('node:assert').throws(() => f([{name:'x',values:new Array(1)}]), TypeError);
