'use strict';
const assert = require('node:assert/strict');
const { makeDependentOptions } = require('./solution');
assert.deepEqual(makeDependentOptions([{group: '', choices: [{code: '', label: 'Empty code'}]}], ''), {
  found: true,
  options: [{value: '', label: '[ CHOOSE AN OPTION ]'}, {value: '', label: 'Empty code'}]
});
