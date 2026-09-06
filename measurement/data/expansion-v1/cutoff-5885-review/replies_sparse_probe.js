'use strict';
const assert = require('node:assert/strict');
const { alignReplies } = require('./solution');
assert.throws(() => alignReplies(new Array(1), []), TypeError);
