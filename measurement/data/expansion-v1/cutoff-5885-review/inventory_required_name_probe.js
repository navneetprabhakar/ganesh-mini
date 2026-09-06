'use strict';
const assert = require('node:assert/strict');
const { findInventoryItem } = require('./solution');
const item = { sku: 'A', name: 'Apple', quantity: 1 };
Object.defineProperty(item, 'name', { value: 'Apple', enumerable: false });
assert.equal(findInventoryItem([item], 'A').name, 'Apple');
