'use strict';
const assert = require('node:assert/strict');
const { pointInsideBeam } = require('./solution');
const point = [1e200, 1e200, 0];
assert.equal(pointInsideBeam({origin: [0, 0, 0], target: point, range: Number.MAX_VALUE, halfAngle: 0}, point), true);
