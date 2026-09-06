'use strict';
const assert = require('node:assert/strict');
const { createLoanBook } = require('./solution');
const book = createLoanBook([
  {member: 'late-a', credits: Number.MAX_VALUE},
  {member: 'late-b', credits: Number.MAX_VALUE},
  {member: 'active-a', credits: 0},
  {member: 'active-b', credits: 0}
]);
book.advance(1);
book.touch('active-a');
book.touch('active-b');
assert.deepEqual(book.redistribute(1), ['late-a', 'late-b']);
assert.equal(book.balance('active-a'), Number.MAX_VALUE);
assert.equal(book.balance('active-b'), Number.MAX_VALUE);
