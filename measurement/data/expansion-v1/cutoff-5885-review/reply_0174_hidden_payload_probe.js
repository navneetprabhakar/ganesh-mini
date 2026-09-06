const assert = require('node:assert/strict');
const { ReplyTracker } = require('./solution');
const tracker = new ReplyTracker(); tracker.begin('id');
const payload = {};
const reply = { id: 'id' };
Object.defineProperty(reply, 'payload', { value: payload, enumerable: false });
assert.deepEqual(tracker.resolve(reply), { id: 'id', payload }, 'Own payload need not be enumerable');
