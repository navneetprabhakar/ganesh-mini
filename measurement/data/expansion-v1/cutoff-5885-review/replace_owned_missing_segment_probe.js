'use strict';
const assert = require('node:assert/strict');
const { replaceOwned } = require('./solution');
assert.throws(() => replaceOwned({}, new Array(1), 1), TypeError);
