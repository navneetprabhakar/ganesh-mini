const assert = require('node:assert/strict');
const { selectPage } = require('./solution');
const pages = {};
Object.defineProperty(pages, 'x', {value:7, enumerable:false});
assert.throws(() => selectPage('x', pages), TypeError);
