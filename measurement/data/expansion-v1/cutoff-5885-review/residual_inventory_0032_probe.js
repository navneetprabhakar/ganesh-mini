const assert = require('node:assert/strict');
const { createInventory } = require('./solution');
assert.throws(() => createInventory(new Array(1)), TypeError);
