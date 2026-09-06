'use strict';
const assert = require('node:assert/strict');
const { createMemberCatalog } = require('./solution');
assert.throws(() => createMemberCatalog().create({id: 'a', displayName: 'A', email: 'a@test', plan: 'p', regions: new Array(1), secret: '12345678'}), TypeError);
