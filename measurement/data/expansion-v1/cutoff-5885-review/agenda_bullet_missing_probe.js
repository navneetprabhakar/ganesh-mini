const {formatAgenda:f}=require('./solution'); require('node:assert').throws(() => f([{heading:'H',bullets:new Array(1)}]), TypeError);
