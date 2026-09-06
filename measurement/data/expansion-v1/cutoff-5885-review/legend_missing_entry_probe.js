'use strict';
const assert = require('node:assert/strict');
const { buildLegend } = require('./solution');
assert.throws(() => buildLegend(new Array(1)), TypeError);
