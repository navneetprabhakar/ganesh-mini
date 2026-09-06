'use strict';
const assert = require('node:assert/strict');
const { radialLayout } = require('./solution');
assert.throws(() => radialLayout(new Array(1)), TypeError);
