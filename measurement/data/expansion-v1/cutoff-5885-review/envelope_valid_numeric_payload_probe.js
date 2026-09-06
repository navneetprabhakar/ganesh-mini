'use strict';
const assert = require('node:assert/strict');
const { createEnvelopeSanitizer } = require('./solution');
const sanitize = createEnvelopeSanitizer(['worker']);
assert.deepStrictEqual(sanitize({ producer: 'worker', headers: { 'trace-id': 't', 'client-version': '1' }, payload: 1 }), {
  ok: true, value: { producer: 'worker', headers: { 'client-version': '1', 'trace-id': 't' }, payload: 1 }
});
