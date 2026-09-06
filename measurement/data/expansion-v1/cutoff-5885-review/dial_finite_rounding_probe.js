'use strict';
const assert = require('node:assert/strict');
const { DecimalDial } = require('./solution');
const value = 1e308;
const dial = new DecimalDial(value, {min: 0, max: Number.MAX_VALUE, step: 1, precision: 1});
// Already an integer, within the accepted finite range. Decimal rounding
// must not replace it with the upper bound through intermediate overflow.
assert.equal(dial.getValue(), value);
