'use strict';
const assert = require('node:assert/strict');
const createRouteTable = require('./solution');
assert.throws(() => createRouteTable(new Array(1)), TypeError);
