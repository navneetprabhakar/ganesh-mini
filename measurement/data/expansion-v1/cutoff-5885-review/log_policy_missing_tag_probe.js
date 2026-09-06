'use strict';
const assert = require('node:assert/strict');
const { createLogPolicy } = require('./solution');
assert.throws(() => createLogPolicy(new Array(1)), TypeError);
