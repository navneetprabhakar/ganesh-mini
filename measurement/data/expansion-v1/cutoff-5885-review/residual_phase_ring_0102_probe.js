const assert = require('node:assert/strict');
const { PhaseRing } = require('./solution');
const phase = new PhaseRing(1, 3, 2).step(Number.MAX_VALUE);
assert.ok(Number.isFinite(phase) && phase >= 0 && phase < 2 * Math.PI, 'finite arguments overflow to NaN instead of wrapped phase');
