const assert = require('node:assert/strict');
const { sumStride } = require('./solution');
assert.throws(() => sumStride(new Array(1), 1, 1), TypeError);
