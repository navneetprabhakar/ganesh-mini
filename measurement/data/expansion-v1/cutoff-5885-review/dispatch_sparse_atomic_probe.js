'use strict';
const assert = require('node:assert/strict');
const { dispatchMessage } = require('./solution');
(async () => {
  let calls = 0;
  const handlers = [() => { calls++; return 'handled'; }];
  handlers.length = 2;
  await assert.rejects(dispatchMessage(handlers, 'message'), TypeError);
  assert.equal(calls, 0);
})().catch(error => { console.error(error); process.exitCode = 1; });
