'use strict';
const assert = require('node:assert/strict');
const { detachRecords } = require('./solution');
assert.throws(() => detachRecords(new Array(1)), TypeError);
