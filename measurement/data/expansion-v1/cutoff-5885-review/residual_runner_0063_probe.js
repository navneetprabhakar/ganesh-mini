const assert = require('node:assert/strict');
const { createTransitionRunner } = require('./solution');
void (async () => {
 const runner = createTransitionRunner(value => value);
 const sequence = [1];
 const marker = new Error('snapshot read failed');
 Object.defineProperty(sequence, 0, {get() {throw marker;}});
 await assert.rejects(runner.run(sequence), error => error === marker);
 assert.equal(runner.isBusy(), false, 'snapshot failure before try/finally leaves runner busy');
 assert.deepEqual(await runner.run([]), {accepted:true,results:[]});
})();
