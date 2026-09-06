const assert = require('node:assert/strict');
const { createEventJournal } = require('./solution');
assert.throws(() => createEventJournal({minimum:['info']}), 'unsupported array minimum must not be coerced to a supported level');
