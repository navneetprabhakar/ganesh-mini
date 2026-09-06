const assert = require('node:assert/strict');
const { renderMeter } = require('./solution');
assert.throws(() => renderMeter(new Array(1), 2), TypeError);
