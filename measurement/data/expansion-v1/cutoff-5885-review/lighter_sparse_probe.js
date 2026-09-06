const assert = require('node:assert/strict');
const { chooseLighter } = require('./solution');
assert.throws(() => chooseLighter(new Array(1), []), TypeError);
