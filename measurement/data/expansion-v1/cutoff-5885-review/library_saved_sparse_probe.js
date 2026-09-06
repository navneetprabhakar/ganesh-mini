const assert = require('node:assert/strict');
const { LibraryNavigator } = require('./solution');
assert.deepEqual(new LibraryNavigator({loans:new Array(1)}).snapshot().loans, []);
