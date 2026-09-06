const assert = require('node:assert/strict');
const { applyCatalogCommand } = require('./solution');
assert.throws(() => applyCatalogCommand({ entries: new Array(1) }, { type: 'ADD', actor: { id: 'e', role: 'editor' }, entry: { id: 'a', title: 'A', quantity: 1 } }), TypeError);
