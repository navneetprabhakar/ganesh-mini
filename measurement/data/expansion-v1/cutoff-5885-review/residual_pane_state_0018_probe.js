'use strict';
const assert = require('node:assert/strict');
const { paneReducer } = require('./solution');
const state = Object.create({left: true, right: true});
const result = paneReducer(state, {type: 'CLOSE_LEFT'});
assert.equal(result.left, false);
assert.equal(result.right, true);
