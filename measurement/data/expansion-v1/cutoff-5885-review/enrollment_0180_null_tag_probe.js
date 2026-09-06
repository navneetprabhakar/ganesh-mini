'use strict';
const assert = require('node:assert/strict');
const { prepareEnrollment } = require('./solution');
assert.throws(() => prepareEnrollment({ name: 'A', email: 'a@b', secret: '12345678', clientTag: null }), TypeError, 'supplied clientTag must be string');
