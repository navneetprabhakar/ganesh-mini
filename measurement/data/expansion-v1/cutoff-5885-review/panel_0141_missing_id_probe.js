'use strict';
const assert = require('node:assert/strict');
const { createAccountPanel } = require('./solution');
assert.throws(() => createAccountPanel({ accounts: {}, requests: {} }, () => {}), TypeError, 'required activeAccountId property is absent');
