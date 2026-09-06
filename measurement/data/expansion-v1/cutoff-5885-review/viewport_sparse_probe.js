'use strict';
const assert = require('node:assert/strict');
const { stableViewportHeight } = require('./solution');
assert.throws(() => stableViewportHeight(new Array(1)), TypeError);
