const assert = require('node:assert/strict');
const renderShipmentTable = require('./solution');
assert.throws(() => renderShipmentTable(new Array(1)), TypeError);
