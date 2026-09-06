'use strict';
const assert = require('node:assert/strict');
const { createPermitRegistry } = require('./solution');
assert.throws(() => createPermitRegistry(new Array(1)), TypeError);
