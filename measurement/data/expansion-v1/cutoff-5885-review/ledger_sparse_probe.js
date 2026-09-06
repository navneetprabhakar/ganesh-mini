'use strict';
const assert = require('node:assert/strict');
const { applyLedgerCredit } = require('./solution');
const accounts = new Array(2);
accounts[0] = {key: 'a', reserve: 0, bonus: 0, tokens: 0};
assert.throws(() => applyLedgerCredit('credit:reserve', 'a', 1, accounts), TypeError);
