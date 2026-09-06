const assert = require('node:assert/strict');
const { authorizeConsoleAttempt } = require('./solution');
assert.throws(() => authorizeConsoleAttempt(new Array(1), {user:'u',token:'t'}), TypeError);
