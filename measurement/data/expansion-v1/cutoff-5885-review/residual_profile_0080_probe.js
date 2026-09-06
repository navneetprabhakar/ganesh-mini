const assert = require('node:assert/strict');
const { validateProfile } = require('./solution');
assert.equal(validateProfile({displayName:'Ab',email:'a@.b.c',biography:'0123456789'}).ok, true, 'domain has an interior dot; existential-dot scope requires disposition');
