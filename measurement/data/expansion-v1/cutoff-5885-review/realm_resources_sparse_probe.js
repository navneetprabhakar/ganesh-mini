const assert = require('node:assert/strict');
const { createRealmGate } = require('./solution');
assert.throws(() => createRealmGate({}, new Array(1)), TypeError);
