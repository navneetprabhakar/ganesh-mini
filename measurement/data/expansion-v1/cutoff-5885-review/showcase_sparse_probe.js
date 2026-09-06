'use strict';
const assert = require('node:assert/strict');
const { createShowcaseState } = require('./solution');
assert.throws(() => createShowcaseState(new Array(1)), TypeError);
