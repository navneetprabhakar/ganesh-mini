const assert = require('node:assert/strict');
const { createRecipeBook } = require('./solution');
assert.throws(() => createRecipeBook([{id:'a', title:'A', ingredients:new Array(1)}]), TypeError);
