const assert = require('node:assert/strict');
const { bearingDegrees } = require('./solution');
const actual = bearingDegrees({ x: -1e308, y: -5e307 }, { x: 1e308, y: 5e307 });
const expected = Math.atan2(1, 2) * 180 / Math.PI;
assert.ok(Math.abs(actual - expected) < 1e-10, 'Finite coordinates: expected ' + expected + ', got ' + actual);
