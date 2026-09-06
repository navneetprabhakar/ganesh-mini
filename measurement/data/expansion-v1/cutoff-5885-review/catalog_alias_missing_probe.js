const {compileCatalog:f}=require('./solution'); require('node:assert').throws(() => f([{code:'x',aliases:new Array(1)}]), TypeError);
