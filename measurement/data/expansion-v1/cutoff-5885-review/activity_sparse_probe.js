const assert = require('node:assert/strict');
const { normalizeActivity } = require('./solution');
assert.throws(() => normalizeActivity({author: {name:'n', avatar:'a'}, ageMinutes:0,
  media:new Array(1), counts:{likes:0,replies:0,shares:0}}), TypeError);
