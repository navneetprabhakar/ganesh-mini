'use strict';
const assert = require('node:assert/strict');
const { createBody, advanceBody } = require('./solution');
const body = createBody({x: 1, y: 2, width: 1, height: 1, mass: Number.MIN_VALUE});
const result = advanceBody(body, {x: 1, y: 1}, 0);
assert.deepEqual(result, body, 'Zero duration must leave finite body values unchanged');
assert.notEqual(result, body);
