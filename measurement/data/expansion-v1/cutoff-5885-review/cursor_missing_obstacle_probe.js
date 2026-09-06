'use strict';
const assert = require('node:assert/strict');
const { advanceCursor } = require('./solution');
assert.throws(() => advanceCursor({ width: 2, height: 1, cursor: { x: 0, y: 0 }, direction: { x: 1, y: 0 }, obstacles: new Array(1) }), TypeError);
