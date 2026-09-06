'use strict';
const assert = require('node:assert/strict');
const { encodeFields } = require('./solution');
assert.throws(() => encodeFields(new Array(1)), TypeError);
