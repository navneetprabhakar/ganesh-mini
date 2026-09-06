'use strict';
const assert = require('node:assert/strict');
const { validateRecord } = require('./solution');
assert.throws(() => validateRecord({}, new Date(0)), TypeError);
