'use strict';
const assert = require('node:assert/strict');
const { renderSessions } = require('./solution');
assert.throws(() => renderSessions({status: 'ready', items: new Array(1)}), TypeError);
