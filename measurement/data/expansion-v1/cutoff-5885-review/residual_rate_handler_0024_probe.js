'use strict';
const assert = require('node:assert/strict');
const { createRateHandler } = require('./solution');
const table = Object.create(null);
table.a = 1;
const handle = createRateHandler(table);
assert.deepEqual(handle({method: 'GET', params: {productId: 'a'}}), {status: 200, body: {productId: 'a', rate: 1}});
