'use strict';
const assert = require('node:assert/strict');
const { buildMemberPage } = require('./solution');
const member = { id: 'a', displayName: 'Ada' };
Object.defineProperty(member, 'displayName', { value: 'Ada', enumerable: false });
assert.equal(buildMemberPage([member], 1, 1, 'a').selected.displayName, 'Ada');
