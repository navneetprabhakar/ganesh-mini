'use strict';
const assert = require('node:assert/strict');
const { buildAccessNotice } = require('./solution');
const state = {signedIn: false, fault: false, displayName: ''};
Object.defineProperty(state, 'extra', {value: 1, enumerable: false});
assert.throws(() => buildAccessNotice(state), TypeError);
