const assert = require('node:assert/strict');
const {renderNotice} = require('./solution');
const data = Object.defineProperty({},'unknown',{value:'x',enumerable:false});
assert.throws(() => renderNotice(data), TypeError);
