'use strict';
const assert = require('node:assert/strict');
const { markKeywords } = require('./solution');
assert.throws(() => markKeywords('text', new Array(1)), TypeError);
