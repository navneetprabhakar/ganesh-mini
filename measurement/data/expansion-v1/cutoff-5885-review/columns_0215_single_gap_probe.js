const assert = require('node:assert/strict');
const { makeColumnPlan } = require('./solution');
assert.equal(makeColumnPlan([1], Number.MAX_VALUE).totalWidth, 1,
  'Single column has no gap; adding and subtracting unused gap loses its width');
