'use strict';
const assert = require('node:assert/strict');
const { planViewport } = require('./solution');
assert.throws(() => planViewport(new Array(1), 0, 1), TypeError);
