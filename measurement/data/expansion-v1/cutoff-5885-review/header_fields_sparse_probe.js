const assert = require('node:assert/strict');
const { headersToFields } = require('./solution');
assert.throws(() => headersToFields(new Array(1)), TypeError);
