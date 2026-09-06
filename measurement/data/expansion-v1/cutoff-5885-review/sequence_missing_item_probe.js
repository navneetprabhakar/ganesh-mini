'use strict';
const assert = require('node:assert/strict');
const { configureSequence } = require('./solution');
assert.throws(() => configureSequence(new Array(1)), TypeError);
