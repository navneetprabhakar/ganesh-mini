'use strict';
const assert = require('node:assert/strict');
const { flattenOutline } = require('./solution');
let root = { id: '12000', children: [] };
for (let i = 11999; i >= 0; i--) root = { id: String(i), children: [root] };
let rows;
try { rows = flattenOutline(root); } catch (error) { throw new Error('valid depth-12000 outline failed: ' + error.name + ': ' + error.message); }
assert.equal(rows.length, 12001);
assert.deepEqual(rows[12000], { id: '12000', depth: 12000 });
