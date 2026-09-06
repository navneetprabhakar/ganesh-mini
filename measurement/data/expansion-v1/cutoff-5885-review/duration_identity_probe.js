'use strict';
const assert = require('node:assert/strict');
const { scaleDuration } = require('./solution');
assert.equal(scaleDuration(Number.MAX_VALUE, 'seconds', 'seconds'), Number.MAX_VALUE);
