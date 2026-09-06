'use strict';
const assert = require('node:assert/strict');
const { renderConceptCards } = require('./solution');
assert.throws(() => renderConceptCards(new Array(1)), TypeError);
