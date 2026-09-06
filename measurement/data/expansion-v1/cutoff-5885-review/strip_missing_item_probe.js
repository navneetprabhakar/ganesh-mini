const assert = require('node:assert/strict');
const { computeStripView } = require('./solution');
assert.throws(() => computeStripView(new Array(1), 0, 1, 'stay'), TypeError);
