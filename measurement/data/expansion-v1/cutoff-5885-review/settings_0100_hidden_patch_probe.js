'use strict';
const assert = require('node:assert/strict');
const { applySettingsPatch } = require('./solution');
const patch = Object.defineProperty({}, 'theme', { value: 7, enumerable: false });
assert.throws(() => applySettingsPatch({ revision: 0, settings: { theme: 'dark', notifications: false } }, patch, 0), TypeError, 'present numeric theme must not bypass validation');
