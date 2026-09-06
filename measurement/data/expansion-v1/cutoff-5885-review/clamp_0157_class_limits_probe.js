const assert = require('node:assert/strict');
const clampGridLevel = require('./solution');
class Limits { constructor() { this.min = 0; this.max = 5; } }
assert.throws(() => clampGridLevel(3, new Limits()), TypeError, 'Limits must be a plain object');
