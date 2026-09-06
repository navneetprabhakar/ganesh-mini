const assert = require('node:assert/strict');
const { buildAlert } = require('./solution');
assert.throws(() => buildAlert({secondary:new Array(1)}), TypeError);
