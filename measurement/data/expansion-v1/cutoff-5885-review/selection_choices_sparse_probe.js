const assert = require('node:assert/strict');
const { summarizeSelections } = require('./solution');
assert.throws(() => summarizeSelections([{respondent:'R', choices:new Array(1)}], ['a']), TypeError);
