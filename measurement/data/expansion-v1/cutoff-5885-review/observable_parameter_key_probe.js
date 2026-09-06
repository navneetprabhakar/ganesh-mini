'use strict';
const assert = require('node:assert/strict');
const { createObservableRecord } = require('./solution');
const record = createObservableRecord({});
record.set('__proto__', 'stored');
assert.equal(record.get('__proto__'), 'stored');
