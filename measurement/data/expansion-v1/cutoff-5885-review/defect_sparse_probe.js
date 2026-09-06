'use strict';
const assert = require('node:assert/strict');
const { handleDefect } = require('./solution');
assert.deepEqual(handleDefect(new Array(1), {type: 'list'}), {status: 400, body: {error: 'Invalid input'}, state: []});
