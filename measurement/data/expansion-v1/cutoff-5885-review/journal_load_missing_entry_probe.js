'use strict';
const assert = require('node:assert/strict');
const reduceJournal = require('./solution');
assert.throws(() => reduceJournal(undefined, { type: 'LOAD_ENTRIES', entries: new Array(1) }), TypeError);
