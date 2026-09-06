'use strict';
const assert = require('node:assert/strict');
const { PartsCatalog } = require('./solution');
const catalog = new PartsCatalog();
const patch = {};
Object.defineProperty(patch, 'extra', { value: true });
assert.throws(() => catalog.update('absent', patch), TypeError);
