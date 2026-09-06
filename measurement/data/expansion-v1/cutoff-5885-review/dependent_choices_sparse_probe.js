'use strict';
const assert = require('node:assert/strict');
const { makeDependentOptions } = require('./solution');
assert.throws(() => makeDependentOptions([{group: 'g', choices: new Array(1)}], 'g'), TypeError);
