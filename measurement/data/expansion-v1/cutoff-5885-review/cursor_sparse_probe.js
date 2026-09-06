'use strict';
const assert = require('node:assert/strict');
const { moveCursor } = require('./solution');
assert.throws(() => moveCursor(new Array(1), 0, 0), TypeError);
