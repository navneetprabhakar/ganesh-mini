'use strict';
const assert = require('node:assert/strict');
const { PreferenceState } = require('./solution');
const state = new PreferenceState({ remoteAllowed: false });
const event = { detail: { value: true } };
Object.defineProperty(event.detail, 'extra', { value: true });
assert.throws(() => state.apply(event), TypeError);
assert.equal(state.snapshot().remoteAllowed, false);
