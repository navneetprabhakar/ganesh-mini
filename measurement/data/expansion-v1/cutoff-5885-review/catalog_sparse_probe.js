'use strict';
const assert = require('node:assert/strict');
const { applyCatalogCommand } = require('./solution');
assert.deepEqual(applyCatalogCommand(new Array(1), {type: 'readAll'}), {status: 400, data: {error: 'Invalid input'}, catalog: []});
