'use strict';
const assert = require('node:assert/strict');
const { summarizeReadings } = require('./solution');
assert.throws(() => summarizeReadings(new Array(1)), TypeError);
