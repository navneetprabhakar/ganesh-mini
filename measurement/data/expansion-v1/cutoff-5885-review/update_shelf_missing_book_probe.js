'use strict';
const assert = require('node:assert/strict');
const { updateShelf } = require('./solution');
assert.throws(() => updateShelf(new Array(1), { type: 'REMOVE', payload: 'x' }), TypeError);
