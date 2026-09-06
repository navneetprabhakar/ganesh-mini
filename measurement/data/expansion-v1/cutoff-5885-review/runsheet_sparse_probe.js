'use strict';
const assert = require('node:assert/strict');
const { createRunSheet } = require('./solution');
const sheet = createRunSheet([{id: 'a', minutes: 1, repeats: 1}]);
assert.throws(() => sheet.replace(new Array(1)), TypeError);
assert.deepEqual(sheet.list(), [{id: 'a', minutes: 1, repeats: 1}]);
