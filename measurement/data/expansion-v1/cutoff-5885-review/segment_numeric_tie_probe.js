const assert = require('node:assert/strict');
const { lowestSegment } = require('./solution');
// Ordinary JS addition rounds (-1e20 + -1) to -1e20: shorter wins.
assert.deepEqual(lowestSegment([1e20, -1e20, -1]), {sum:-1e20, start:1, end:1});
