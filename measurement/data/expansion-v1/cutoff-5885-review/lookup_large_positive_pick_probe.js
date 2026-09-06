const assert = require('node:assert/strict');
const { interpretLookup } = require('./solution');
assert.equal(interpretLookup('/pick:9007199254740992 q', []), 'No results.');
