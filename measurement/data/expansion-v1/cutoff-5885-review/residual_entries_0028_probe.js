const assert = require('node:assert/strict');
const { entriesToRecord } = require('./solution');
assert.deepEqual(Object.keys(entriesToRecord([['2', 'b'], ['1', 'a']])), ['2', '1']);
