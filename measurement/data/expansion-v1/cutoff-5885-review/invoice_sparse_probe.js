'use strict';
const assert = require('node:assert/strict');
const { calculateInvoice } = require('./solution');
assert.throws(() => calculateInvoice(new Array(1)), TypeError);
