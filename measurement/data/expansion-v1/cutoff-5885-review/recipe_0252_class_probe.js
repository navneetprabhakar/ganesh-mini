const assert = require('node:assert/strict');
const { createRecipeEditor } = require('./solution');
class Recipe { constructor() { this.name = 'Soup'; this.instructions = 'Boil'; } }
assert.throws(() => createRecipeEditor(new Recipe(), () => {}), TypeError, 'Initial recipe must be plain');
