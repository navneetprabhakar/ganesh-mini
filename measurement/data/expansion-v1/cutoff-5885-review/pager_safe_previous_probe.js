'use strict';
const assert = require('node:assert/strict');
const { reducePager } = require('./solution');
assert.deepEqual(reducePager({ page: 3, pageCount: Number.MAX_SAFE_INTEGER, revision: 0 },
  { type: 'previous' }), { page: 2, pageCount: Number.MAX_SAFE_INTEGER, revision: 1 });
