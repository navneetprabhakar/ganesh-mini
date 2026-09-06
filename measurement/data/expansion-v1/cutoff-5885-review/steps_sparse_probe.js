'use strict';
const assert = require('node:assert/strict');
const { labelSteps } = require('./solution');
assert.rejects(() => labelSteps(new Array(1)), TypeError).catch(error => { console.error(error); process.exitCode = 1; });
