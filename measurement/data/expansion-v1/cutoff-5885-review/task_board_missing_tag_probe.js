'use strict';
const assert = require('node:assert/strict');
const { createTaskBoard } = require('./solution');
assert.throws(() => createTaskBoard().add({ id: 'a', title: 'Alpha', priority: 1, tags: new Array(1) }));
