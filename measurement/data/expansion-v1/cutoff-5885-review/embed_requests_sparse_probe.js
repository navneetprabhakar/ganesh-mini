const assert = require('node:assert/strict');
const { createEmbedDescriptors } = require('./solution');
assert.throws(() => createEmbedDescriptors('https://example.com', new Array(1)), TypeError);
