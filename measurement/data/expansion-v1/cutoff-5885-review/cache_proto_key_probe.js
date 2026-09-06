'use strict';
const assert = require('node:assert/strict');
const { touchAssetCache } = require('./solution');
const result = touchAssetCache({order: [], entries: {}}, '__proto__', 'asset', 1);
assert.deepEqual(result.order, ['__proto__']);
assert.equal(Object.hasOwn(result.entries, '__proto__'), true);
assert.equal(result.entries.__proto__, 'asset');
