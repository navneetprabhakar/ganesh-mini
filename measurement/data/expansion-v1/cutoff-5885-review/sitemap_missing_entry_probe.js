const assert = require('node:assert/strict');
const { buildSiteMap } = require('./solution');
assert.throws(() => buildSiteMap('Brand', new Array(1), 640), TypeError);
