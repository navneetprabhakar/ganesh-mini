'use strict';
const assert = require('node:assert/strict');
const { renderKnowledgePage } = require('./solution');
assert.throws(() => renderKnowledgePage({title: 'T', description: 'D', published: 'P', slug: 'S', minutes: 1, paragraphs: new Array(1), tags: []}), TypeError);
