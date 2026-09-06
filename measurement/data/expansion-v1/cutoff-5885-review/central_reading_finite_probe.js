'use strict';
const assert = require('node:assert/strict');
const { centralReading } = require('./solution');
assert.equal(centralReading([Number.MAX_VALUE, Number.MAX_VALUE]), Number.MAX_VALUE);
