'use strict';
const assert = require('node:assert/strict');
const { serializeSafeRow } = require('./solution');
assert.throws(() => serializeSafeRow(new Array(1)), TypeError);
