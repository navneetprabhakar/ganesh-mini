const assert = require('node:assert/strict');
const { createAccessRegistry } = require('./solution');
const details = { email: 'a@b', secret: 's', givenName: 'A', familyName: 'B' };
Object.defineProperty(details, 'givenName', { value: 'A', enumerable: false });
assert.equal(createAccessRegistry().register(details).givenName, 'A');
