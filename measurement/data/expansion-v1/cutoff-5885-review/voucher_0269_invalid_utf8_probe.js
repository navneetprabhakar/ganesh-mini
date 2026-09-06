const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const verifyVoucher = require('./solution');
const bytes = Buffer.concat([Buffer.from('{"subject":"'), Buffer.from([0xff]), Buffer.from('","expiresAt":10}')]);
const body = bytes.toString('base64url');
const secret = 'probe-secret';
const signature = crypto.createHmac('sha256', secret).update(body).digest('base64url');
assert.rejects(verifyVoucher(body + '.' + signature, secret, 0),
  'Body is not UTF-8 JSON and must not be silently repaired').catch(error => { console.error(error); process.exitCode = 1; });
