const assert = require('node:assert/strict');
const { moveViewport } = require('./solution');
const n = Number.MAX_SAFE_INTEGER;
assert.equal(moveViewport(n - 2, 'backward', n), n - 3);
