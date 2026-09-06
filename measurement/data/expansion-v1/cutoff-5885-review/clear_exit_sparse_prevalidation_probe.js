const assert = require('node:assert/strict');
const { clearAndExit } = require('./solution');
async function main() {
  let calls = 0;
  await assert.rejects(clearAndExit({remove() { calls++; }}, {go() { calls++; }}, new Array(1), '/done'), TypeError);
  assert.equal(calls, 0, 'Malformed input must not call collaborators');
}
main().catch(error => { throw error; });
