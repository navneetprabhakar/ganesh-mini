const assert = require('node:assert/strict');
const { traceCapacity } = require('./solution');
assert.throws(() => traceCapacity(1, new Array(1)), TypeError);
