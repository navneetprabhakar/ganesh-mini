'use strict';
const assert = require('node:assert/strict');
const { createDocumentIndex } = require('./solution');
assert.throws(() => createDocumentIndex([{ code: 'A', title: 'Title', state: 'draft', labels: new Array(1) }]), TypeError);
