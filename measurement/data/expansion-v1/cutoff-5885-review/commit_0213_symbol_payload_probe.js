const assert = require('node:assert/strict');
const { createCommitGate } = require('./solution');
const key = Symbol('payload');
const nested = {};
const gate = createCommitGate(() => true);
assert.throws(() => gate.stage({ [key]: nested }), TypeError,
  'Own symbol value is an unsupported object and must not be retained');
