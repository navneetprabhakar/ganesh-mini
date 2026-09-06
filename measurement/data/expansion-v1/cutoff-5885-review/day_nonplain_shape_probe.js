'use strict';
const assert = require('node:assert/strict');
const { makeDayChosenEvent } = require('./solution');
class Day { constructor() { this.year = 2024; this.month = 2; this.day = 29; } }
assert.throws(() => makeDayChosenEvent(new Day()), TypeError);
