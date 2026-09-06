'use strict';
const assert = require('node:assert/strict');
const { createFeelingState, reduceFeelingState } = require('./solution');
const state = createFeelingState();
Object.defineProperty(state, 'feeling', { value: 'calm', enumerable: false });
assert.equal(reduceFeelingState(state, { type: 'toggle-state' }, () => {}).feeling, 'calm', 'toggle must retain validated feeling');
