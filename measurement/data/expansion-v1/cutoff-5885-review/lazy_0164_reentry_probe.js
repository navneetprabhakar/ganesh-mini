'use strict';
const assert = require('node:assert/strict');
const { createLazyValue } = require('./solution');
let calls = 0;
let nested;
const lazy = createLazyValue(() => {
  calls++;
  if (calls === 1) nested = lazy.read();
  return 42;
});
const outer = lazy.read();
assert.equal(calls, 1, 'overlapping reads must share one loader invocation');
assert.strictEqual(outer, nested, 'overlapping reads share pending Promise');
