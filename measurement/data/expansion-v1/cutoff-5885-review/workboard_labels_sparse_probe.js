'use strict';
const assert = require('node:assert/strict');
const { buildWorkBoard } = require('./solution');
assert.throws(() => buildWorkBoard([{type: 'add', id: 'a', summary: 'A', severity: 'standard', labels: new Array(1)}]));
