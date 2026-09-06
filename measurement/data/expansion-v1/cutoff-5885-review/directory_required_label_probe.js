'use strict';
const assert = require('node:assert/strict');
const { applyDirectoryCommand } = require('./solution');
const record = { id: 'a', label: 'Ada', contact: 'a@example.test' };
Object.defineProperty(record, 'label', { value: 'Ada', enumerable: false });
assert.equal(applyDirectoryCommand([record], { type: 'GET', id: 'a' }).record.label, 'Ada');
