const assert = require('node:assert/strict');
const { runSteps } = require('./solution');
async function main() {
  let runs = 0;
  const steps = new Array(2); steps[0] = () => { runs++; };
  await assert.rejects(runSteps(steps), TypeError);
  assert.equal(runs, 0, 'All elements must be validated before any step runs');
}
main().catch(error => { throw error; });
