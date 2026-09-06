const assert = require('node:assert/strict');
const { selectCandidates } = require('./solution');
assert.throws(() => selectCandidates(new Array(1), {}), TypeError);
