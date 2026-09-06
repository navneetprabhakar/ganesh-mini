const {registerTopic} = require('./solution');
require('node:assert').throws(() => registerTopic([{label:' x ',createdIndex:0,purpose:'discussion'}], 'x', 1), RangeError);
