'use strict';
const assert = require('node:assert/strict');
const { selectBuildPages } = require('./solution');
assert.throws(() => selectBuildPages([], new Array(1)), TypeError);
