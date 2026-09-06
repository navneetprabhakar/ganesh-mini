const assert = require('node:assert/strict');
const { validateAccessRequest } = require('./solution');
const result = validateAccessRequest({displayName:'A', department:'D', location:'L', phone:'bad', email:'a@b', pin:'A12345', pinConfirmation:''});
assert.deepEqual(Object.keys(result.errors), ['phone', 'pinConfirmation']);
