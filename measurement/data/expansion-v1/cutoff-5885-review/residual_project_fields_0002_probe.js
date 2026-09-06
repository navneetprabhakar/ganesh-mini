'use strict';
const assert = require('node:assert/strict');
const { projectFields } = require('./solution');
const source = JSON.parse('{"__proto__":{"x":1},"normal":2}');
const result = projectFields(source, []);
assert.deepEqual(Object.keys(result), Object.keys(source));
assert.equal(Object.getPrototypeOf(result), Object.prototype);
