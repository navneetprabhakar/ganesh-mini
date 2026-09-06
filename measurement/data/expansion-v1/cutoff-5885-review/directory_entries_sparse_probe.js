'use strict';
const assert = require('node:assert/strict');
const { makeDirectory } = require('./solution');
assert.throws(() => makeDirectory(new Array(1)), TypeError);
