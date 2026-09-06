'use strict';
const assert = require('node:assert/strict');
const { drawRoute } = require('./solution');
class Point { constructor() { this.x = 0; this.y = 0; } }
assert.throws(() => drawRoute(1, 1, [new Point()]), TypeError);
