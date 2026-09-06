'use strict';
const assert = require('node:assert/strict');
const { createParcelRegistry } = require('./solution');
assert.throws(() => createParcelRegistry().list({ limit: Infinity }), TypeError);
