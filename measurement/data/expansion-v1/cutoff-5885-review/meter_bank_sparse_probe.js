const assert = require('node:assert/strict');
const { createMeterBank } = require('./solution');
assert.throws(() => createMeterBank(new Array(1)), TypeError);
