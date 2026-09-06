'use strict';
const assert = require('node:assert/strict');
const { appendBatch } = require('./solution');
const added = new Array(200000).fill(7);
let result;
try { result = appendBatch([1], added); } catch (error) { throw new Error('valid 200000-item append failed: ' + error.name + ': ' + error.message); }
assert.equal(result.length, 200001);
assert.equal(result[200000], 7);
