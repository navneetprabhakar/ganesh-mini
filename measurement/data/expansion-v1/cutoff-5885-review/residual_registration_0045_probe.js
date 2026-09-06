const assert = require('node:assert/strict');
const { RegistrationValidator } = require('./solution');
assert.deepEqual(RegistrationValidator.validate({handle:'a', contact:'a@b.c.', passphrase:'abcdefghI9'}), []);
