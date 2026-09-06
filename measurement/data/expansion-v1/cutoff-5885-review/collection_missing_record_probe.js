'use strict';
const assert = require('node:assert/strict');
const { buildCollectionView } = require('./solution');
assert.throws(() => buildCollectionView('Catalog', new Array(1)), TypeError);
