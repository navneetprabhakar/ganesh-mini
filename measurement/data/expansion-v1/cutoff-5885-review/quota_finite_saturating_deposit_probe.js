'use strict';
const assert = require('node:assert/strict');
const { QuotaPool } = require('./solution');
const pool = new QuotaPool(Number.MAX_VALUE, Number.MAX_VALUE);
assert.equal(pool.deposit(Number.MAX_VALUE), Number.MAX_VALUE);
