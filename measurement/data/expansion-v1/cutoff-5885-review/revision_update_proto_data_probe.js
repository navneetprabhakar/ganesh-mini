'use strict';
const assert = require('node:assert/strict');
const { prepareRevisionUpdate } = require('./solution');
const input = JSON.parse('{"metadata":{"__proto__":{"flag":true}}}');
const result = prepareRevisionUpdate(input);
assert.deepEqual(Object.keys(result.metadata), ['__proto__']);
assert.equal(result.metadata.__proto__.flag, true);
