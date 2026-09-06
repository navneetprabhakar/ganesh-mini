'use strict';
const assert = require('node:assert/strict');
const { listStations } = require('./solution');
assert.throws(() => listStations({x: new Array(1)}, 'x'), TypeError);
