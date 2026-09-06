const assert = require('node:assert/strict');
const { countUnits } = require('./solution');
const big = 2 ** 53;
assert.equal(countUnits({a:big,b:1,c:1}), countUnits({b:1,c:1,a:big}), 'Object key order must not affect total');
