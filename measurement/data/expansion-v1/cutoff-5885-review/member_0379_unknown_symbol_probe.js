const assert = require('node:assert/strict');
const {updateMember} = require('./solution');
const patch = {[Symbol('unknown')]:{mutable:true}};
assert.throws(() => updateMember([{id:'a'}], 'a', patch), TypeError);
