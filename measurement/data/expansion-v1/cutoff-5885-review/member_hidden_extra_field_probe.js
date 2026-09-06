'use strict';
const assert = require('node:assert/strict');
const { MemberDirectory } = require('./solution');
const group = { id: 'g', name: 'Group' };
Object.defineProperty(group, 'extra', { value: true });
const member = { id: 'm', name: 'Member', age: 1, pronoun: 'p', address: 'a', groupId: 'g' };
assert.throws(() => new MemberDirectory([group], [member]), TypeError);
