'use strict';
const assert = require('node:assert/strict');
const { resizeTextRuns } = require('./solution');
assert.throws(() => resizeTextRuns(new Array(1), 12), TypeError);
