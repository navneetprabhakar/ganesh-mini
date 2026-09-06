'use strict';
const assert = require('node:assert/strict');
const { packSegments } = require('./solution');
assert.throws(() => packSegments(new Array(1)), TypeError);
