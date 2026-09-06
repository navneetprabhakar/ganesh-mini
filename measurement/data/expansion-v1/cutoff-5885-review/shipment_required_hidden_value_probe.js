'use strict';
const assert = require('node:assert/strict');
const { calculateUnexplained } = require('./solution');
const data = { completed: 0, delayed: 0, damaged: 0, waived: 0 };
Object.defineProperty(data, 'received', { value: 1 });
assert.equal(calculateUnexplained(data), 1);
