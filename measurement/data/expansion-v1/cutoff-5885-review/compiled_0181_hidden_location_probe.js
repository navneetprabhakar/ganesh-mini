'use strict';
const assert = require('node:assert/strict');
const { packCompiledRecords } = require('./solution');
const record = { location: '/base/a', source: 'text', format: 'compiled' };
Object.defineProperty(record, 'location', { value: '/base/a', enumerable: false });
const result = packCompiledRecords([record], { makeKey: () => 0, debug: false, base: '/base' });
assert.equal(result[0][0].location, '/base/a', 'copied record lost required location');
