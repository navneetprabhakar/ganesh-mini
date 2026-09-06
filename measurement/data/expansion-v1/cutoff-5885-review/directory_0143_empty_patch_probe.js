'use strict';
const assert = require('node:assert/strict');
const { createMemberDirectory } = require('./solution');
const d = createMemberDirectory();
const before = d.create({ id: 'a', displayName: 'A', contact: 'c', secret: 's' });
const after = d.update('a', {});
assert.deepEqual(after, before);
assert.notStrictEqual(after, before);
