'use strict';
const assert = require('node:assert/strict');
const { buildMenu } = require('./solution');
assert.throws(() => buildMenu(new Array(1)), TypeError);
