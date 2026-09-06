'use strict';
const assert = require('node:assert/strict');
const { prismVolume } = require('./solution');
assert.equal(prismVolume(Number.MAX_VALUE, 2, 0), 0);
