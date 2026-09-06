'use strict';
const assert = require('node:assert/strict');
const { createRecipeBook } = require('./solution');
const recipe = {name: 'A', servings: 1, vegetarian: true};
Object.defineProperty(recipe, 'extra', {value: 1, enumerable: false});
assert.throws(() => createRecipeBook().add(recipe), TypeError);
