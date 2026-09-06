const assert = require('node:assert/strict');
const { stockReducer, receive } = require('./solution');
const result = stockReducer({units:Number.MAX_VALUE}, receive(Number.MAX_VALUE));
assert.equal(Number.isInteger(result.units), true, 'accepted integer inputs produce noninteger Infinity; numeric envelope requires disposition');
