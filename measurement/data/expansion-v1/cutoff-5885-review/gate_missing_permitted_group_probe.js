'use strict';
const assert = require('node:assert/strict');
const { createGate } = require('./solution');
assert.throws(() => createGate(new Array(1)), TypeError);
