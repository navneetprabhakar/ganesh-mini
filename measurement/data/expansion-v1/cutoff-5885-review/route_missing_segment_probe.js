'use strict';
const assert = require('node:assert/strict');
const { encodeRoute } = require('./solution');
assert.throws(() => encodeRoute(new Array(1)), TypeError);
