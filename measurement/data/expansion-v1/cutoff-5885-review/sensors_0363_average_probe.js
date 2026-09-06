const assert = require('node:assert/strict');
const { summarizeSensors } = require('./solution');
const result = summarizeSensors([{zone:'a', value:Number.MAX_VALUE}, {zone:'a', value:Number.MAX_VALUE}]);
console.log('average', String(result.a.average));
assert.equal(result.a.average, Number.MAX_VALUE);
