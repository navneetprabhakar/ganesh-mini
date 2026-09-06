const assert = require('node:assert/strict');
const { parseLedger } = require('./solution');
const m = Number.MAX_SAFE_INTEGER;
assert.equal(parseLedger(`a=${m};b=2;c=${-m}`).total, 2);
