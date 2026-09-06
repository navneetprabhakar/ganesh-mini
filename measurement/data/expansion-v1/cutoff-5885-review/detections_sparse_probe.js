const assert = require('node:assert/strict');
const { inspectDetections } = require('./solution');
assert.throws(() => inspectDetections(new Array(1), 'x', 0), TypeError);
