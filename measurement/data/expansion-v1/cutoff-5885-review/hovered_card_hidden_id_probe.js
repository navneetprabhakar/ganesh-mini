const assert = require('node:assert/strict');
const { setHovered } = require('./solution');
const card = {id:'a',label:'A',accent:'red'};
Object.defineProperty(card, 'id', {enumerable:false});
assert.equal(setHovered([card], 'a', true)[0].id, 'a');
