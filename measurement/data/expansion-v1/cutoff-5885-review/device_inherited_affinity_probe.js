'use strict';
const assert = require('node:assert/strict');
const { summarizeDevice } = require('./solution');
const result = summarizeDevice('X', [{ name: 'X', id: 1, categories: ['__proto__'], metrics: {} }], {});
assert.deepEqual(result.helpedBy, []);
assert.deepEqual(result.hinderedBy, []);
