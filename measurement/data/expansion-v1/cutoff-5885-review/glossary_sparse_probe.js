'use strict';
const assert = require('node:assert/strict');
const { createGlossary } = require('./solution');
const failures = [];
for (const [name, action] of [
  ['categories', () => createGlossary([{term: 'valid', categories: new Array(1)}])],
  ['tokens', () => createGlossary([]).review(new Array(1))],
]) {
  try { action(); failures.push(name); }
  catch (error) { if (!(error instanceof TypeError)) throw error; }
}
assert.deepEqual(failures, [], 'sparse inputs accepted');
