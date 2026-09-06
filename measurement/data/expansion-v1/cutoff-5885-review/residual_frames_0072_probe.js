const assert = require('node:assert/strict');
const { decodeFrames } = require('./solution');
const input = Buffer.from([0, 1, 7]);
assert.ok(input instanceof Uint8Array);
const output = decodeFrames(input);
assert.equal(output.ok, true);
output.frames[0][0] = 9;
assert.equal(input[2], 7, 'Buffer is a Uint8Array but its slice aliases input bytes');
