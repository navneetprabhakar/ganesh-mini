const assert = require('node:assert/strict');
const { summarizeServiceOrders } = require('./solution');
assert.throws(() => summarizeServiceOrders(new Array(1), 0), TypeError);
