'use strict';
const assert = require('node:assert/strict');
const { resolveAccess } = require('./solution');
assert.throws(() => resolveAccess([], { resource: 'r', action: 'a', groups: new Array(1) }), TypeError);
