'use strict';
const assert = require('node:assert/strict');
const { reduceWarehouse } = require('./solution');
assert.throws(() => reduceWarehouse({ draft: {}, items: [] }, { type: 'REPLACE_ITEMS', items: new Array(1) }), TypeError);
