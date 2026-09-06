'use strict';
const assert = require('node:assert/strict');
const { stableViewportHeight } = require('./solution');
assert.equal(stableViewportHeight([Number.MAX_VALUE, Number.MAX_VALUE]), Number.MAX_VALUE);
