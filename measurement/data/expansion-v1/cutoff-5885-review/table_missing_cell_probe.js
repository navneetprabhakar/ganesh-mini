'use strict';
const assert = require('node:assert/strict');
const { encodeTable } = require('./solution');
assert.throws(() => encodeTable([new Array(1)]), TypeError);
