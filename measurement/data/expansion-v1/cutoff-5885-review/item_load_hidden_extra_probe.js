const assert = require('node:assert/strict');
const { initialLoadState, reduceItemLoad } = require('./solution');
const event = { type: 'START' };
Object.defineProperty(event, 'extra', { value: 1, enumerable: false });
assert.throws(() => reduceItemLoad(initialLoadState, event), TypeError);
