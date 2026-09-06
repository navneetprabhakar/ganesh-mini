'use strict';
const assert = require('node:assert/strict');
const { highestPriority } = require('./solution');
assert.throws(() => highestPriority(new Array(1)), TypeError);
