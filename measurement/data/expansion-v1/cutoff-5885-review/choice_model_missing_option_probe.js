'use strict';
const assert = require('node:assert/strict');
const { createChoiceModel } = require('./solution');
assert.throws(() => createChoiceModel(new Array(1)), TypeError);
