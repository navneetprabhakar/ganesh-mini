'use strict';
const assert = require('node:assert/strict');
const { createDisclosureModel } = require('./solution');
assert.throws(() => createDisclosureModel(new Array(1)), TypeError);
