const assert = require('node:assert/strict');
const { createRecipeBook } = require('./solution');
async function run() {
  const events = [];
  const book = createRecipeBook(event => events.push(event));
  await assert.rejects(book.add({ key: 'k', title: 'valid', ingredients: new Array(1) }), TypeError);
  assert.equal(await book.get('k'), null);
}
run().catch(error => { throw error; });
