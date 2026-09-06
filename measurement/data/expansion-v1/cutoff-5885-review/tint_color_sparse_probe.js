const assert = require('node:assert/strict');
const { tintMask } = require('./solution');
assert.throws(() => tintMask(new Uint8ClampedArray(0), new Array(3)), TypeError);
