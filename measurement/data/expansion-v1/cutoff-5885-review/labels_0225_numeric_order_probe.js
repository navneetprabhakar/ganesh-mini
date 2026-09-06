const assert = require('node:assert/strict');
const { buildLabelIndex } = require('./solution');
assert.deepEqual(Object.keys(buildLabelIndex(['2', '1'])), ['2', '1'],
  'Canonical numeric keys must enumerate in first-appearance order');
