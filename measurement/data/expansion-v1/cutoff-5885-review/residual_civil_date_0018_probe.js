'use strict';
const assert = require('node:assert/strict');
const { formatCivilDate } = require('./solution');
const date = {year: 2024, month: 1, day: 1};
Object.defineProperty(date, 'extra', {value: 1, enumerable: false});
assert.throws(() => formatCivilDate(date), TypeError);
