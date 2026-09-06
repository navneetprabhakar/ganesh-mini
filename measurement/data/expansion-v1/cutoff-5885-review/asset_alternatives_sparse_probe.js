'use strict';
const assert = require('node:assert/strict');
const { chooseAsset } = require('./solution');
assert.throws(() => chooseAsset('primary', new Array(1)), TypeError);
