const assert = require('node:assert/strict');
const { projectScalarPaths } = require('./solution');
assert.throws(() => projectScalarPaths({}, [{key:'x',path:new Array(1)}]), TypeError);
