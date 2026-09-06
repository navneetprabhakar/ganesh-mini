const assert = require('node:assert/strict');
const { sharedLabels } = require('./solution');
assert.throws(() => sharedLabels(new Array(1), []), TypeError);
