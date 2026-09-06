'use strict';
const assert = require('node:assert/strict');
const renderTokens = require('./solution');
assert.throws(() => renderTokens(new Array(1)), TypeError);
