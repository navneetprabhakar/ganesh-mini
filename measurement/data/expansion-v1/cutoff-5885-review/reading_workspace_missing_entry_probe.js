'use strict';
const assert = require('node:assert/strict');
const { buildReadingWorkspace } = require('./solution');
assert.throws(() => buildReadingWorkspace('Review', new Array(1)), TypeError);
