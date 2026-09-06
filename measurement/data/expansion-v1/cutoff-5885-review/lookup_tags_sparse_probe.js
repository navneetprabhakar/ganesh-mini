'use strict';
const assert = require('node:assert/strict');
const { LookupValue } = require('./solution');
assert.throws(() => new LookupValue('id', 'label', new Array(1)), TypeError);
