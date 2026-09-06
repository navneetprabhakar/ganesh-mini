'use strict';
const assert = require('node:assert/strict');
const { validateWorkshopRequest } = require('./solution');
assert.throws(() => validateWorkshopRequest('Topic', 2.5, 'fac-123456'), RangeError, 'number with out-of-contract form is correctly typed but outside the permitted range/form');
