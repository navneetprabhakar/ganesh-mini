'use strict';
const assert = require('node:assert/strict');
const toggle = require('./solution');
const state = JSON.parse('{"__proto__":false,"other":true}');
const result = toggle(state, '__proto__');
assert.deepEqual(Object.keys(result), ['__proto__', 'other']);
assert.equal(result.__proto__, true);
assert.equal(result.other, false);
