const assert = require('node:assert/strict');
const { summarizeDurations } = require('./solution');
assert.deepEqual(Object.keys(summarizeDurations(['2 10', '1 20'])), ['2', '1'],
  'Numeric operation names must retain first-seen order');
