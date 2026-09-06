'use strict';
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const { authorizePass } = require('./solution');
const encoded = Buffer.from(JSON.stringify({subject: 'u', role: 'r', expires: 100})).toString('base64url');
const ticket = encoded + '.' + crypto.createHmac('sha256', 'entry').update(encoded).digest('hex');
const headers = {};
Object.defineProperty(headers, 'X-Entry-Pass', {value: ticket, enumerable: false});
assert.deepEqual(authorizePass({headers, now: 1}, {entryKey: 'entry', renewalKey: 'renewal'}), {ok: true, status: 200, role: 'r'});
