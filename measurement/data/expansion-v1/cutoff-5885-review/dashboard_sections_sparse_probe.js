'use strict';
const assert = require('node:assert/strict');
const { composeDashboard } = require('./solution');
assert.throws(() => composeDashboard(new Array(1), 640), TypeError);
