'use strict';
const assert = require('node:assert/strict');
const { createPolicyEvaluator } = require('./solution');
assert.throws(() => createPolicyEvaluator([{ principal: 'p', resource: 'r', actions: new Array(1) }]), TypeError);
