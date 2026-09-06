const assert = require('node:assert/strict');
const { runConcurrentInOrder } = require('./solution');
assert.throws(() => runConcurrentInOrder(new Array(1)), TypeError);
