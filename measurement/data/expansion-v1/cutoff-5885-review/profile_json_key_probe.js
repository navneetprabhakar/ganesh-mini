'use strict';
const assert = require('node:assert/strict');
const { createProfileRepository } = require('./solution');
const source = JSON.parse('{"id":"x","__proto__":{"label":"original"},"name":"original"}');
const repo = createProfileRepository([source]);
const first = repo.get('x');
first.name = 'mutated';
assert.equal(repo.get('x').name, 'original', 'JSON-key cloning must not leak stored record');
