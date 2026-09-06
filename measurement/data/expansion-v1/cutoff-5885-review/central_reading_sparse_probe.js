'use strict';
const assert = require('node:assert/strict');
const { centralReading } = require('./solution');
assert.throws(() => centralReading(new Array(1)), TypeError);
