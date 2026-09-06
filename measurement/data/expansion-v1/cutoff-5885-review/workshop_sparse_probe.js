const assert = require('node:assert/strict');
const { formatWorkshop } = require('./solution');
assert.throws(() => formatWorkshop({title:'valid',seats:1,topics:new Array(1)}), TypeError);
