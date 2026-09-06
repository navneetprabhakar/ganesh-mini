'use strict';
const assert = require('node:assert/strict');
const { priceOrderLines } = require('./solution');
assert.throws(() => priceOrderLines([], new Array(1)), TypeError);
