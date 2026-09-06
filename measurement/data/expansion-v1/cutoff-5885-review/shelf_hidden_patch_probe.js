'use strict';
const assert = require('node:assert/strict');
const createReadingShelf = require('./solution');
const shelf = createReadingShelf([{id: 1, title: 'A', pages: 1, status: 'planned'}]);
const patch = {};
Object.defineProperty(patch, 'unexpected', {value: true, enumerable: false});
assert.throws(() => shelf.update(1, patch), TypeError);
