'use strict';
const assert = require('node:assert/strict');
const { moveRobot } = require('./solution');
assert.throws(() => moveRobot([[0]], { row: 0, column: 0 }, new String('N')), TypeError);
