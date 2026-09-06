const {summarizeQueues}=require('./solution');
require('node:assert').throws(() => summarizeQueues([],new Array(1)),TypeError);
