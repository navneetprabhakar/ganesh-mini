const assert = require('node:assert/strict');
const { createSession } = require('./solution');
const names = new Array(2); names[1] = 'Bob';
assert.throws(() => createSession(names), TypeError);
