const assert = require('node:assert/strict');
const { isRightTriangle } = require('./solution');
assert.equal(isRightTriangle([1, Number.MAX_SAFE_INTEGER, Number.MAX_SAFE_INTEGER]), false);
