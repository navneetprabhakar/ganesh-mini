'use strict';
const assert = require('node:assert/strict');
const { createControlBoard } = require('./solution');
const board = createControlBoard({ entries: [{ key: '__proto__', kind: 'text', initial: 'value' }] });
assert.deepEqual(Object.keys(board.getState()), ['__proto__']);
assert.equal(board.getState().__proto__, 'value');
