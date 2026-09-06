const assert = require('node:assert/strict');
const { createSelectionModel } = require('./solution');
assert.throws(() => createSelectionModel(new Array(1)), TypeError);
