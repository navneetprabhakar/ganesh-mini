'use strict';
const assert = require('node:assert/strict');
const runningTotals = require('./solution');
assert.throws(() => runningTotals(new Array(1)), TypeError);
