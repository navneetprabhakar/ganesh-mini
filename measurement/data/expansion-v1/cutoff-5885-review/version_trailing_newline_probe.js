'use strict';
const assert = require('node:assert/strict');
const { compareVersions } = require('./solution');
assert.throws(() => compareVersions('1\n', '1'), TypeError);
