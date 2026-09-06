'use strict';
const assert = require('node:assert/strict');
const { runPipeline } = require('./solution');
(async () => {
  let calls = 0;
  const steps = [value => { calls++; return value; }];
  steps.length = 2;
  await assert.rejects(runPipeline(0, steps), TypeError);
  assert.equal(calls, 0, 'Validation must precede every step invocation');
})().catch(error => { console.error(error); process.exitCode = 1; });
