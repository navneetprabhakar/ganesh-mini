'use strict';
const assert = require('node:assert/strict');
const { applyFieldUpdates } = require('./solution');
assert.throws(() => applyFieldUpdates({ [Symbol('not-string')]: 1 }, []), TypeError, 'own keys must be safe strings');
