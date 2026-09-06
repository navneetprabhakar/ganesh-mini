const assert = require('node:assert/strict');
const { chunkBytes } = require('./solution');
const chunks = chunkBytes(new Uint8Array([1,2]), 1);
assert.deepEqual(chunks.map((chunk,index) => index), [0,1], 'Returned chunk array must retain ordinary map behavior');
