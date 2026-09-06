'use strict';
const assert = require('node:assert/strict');
const { makeBookSummary } = require('./solution');
assert.throws(() => makeBookSummary({ title: 'T', authors: new Array(1), pageCount: 1 }), TypeError);
