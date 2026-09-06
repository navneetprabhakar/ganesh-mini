'use strict';
const assert = require('node:assert/strict');
const { pointInsideBeam } = require('./solution');
assert.throws(() => pointInsideBeam({origin: [0, 0, 0], target: [1, 0, 0], range: 1, halfAngle: 0}, new Array(3)), TypeError);
