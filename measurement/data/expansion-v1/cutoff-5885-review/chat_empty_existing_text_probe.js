const assert = require('node:assert/strict');
const { applyChatAction } = require('./solution');
assert.throws(() => applyChatAction({ draft: '', messages: [{ id: 'm', sender: 's', text: '' }] }, { type: 'EDIT', text: 'new' }), TypeError);
