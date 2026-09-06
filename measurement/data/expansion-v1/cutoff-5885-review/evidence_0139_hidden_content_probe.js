'use strict';
const assert = require('node:assert/strict');
const { partitionEvidence } = require('./solution');
const record = { id: 'a', kind: 'note', content: 'text' };
Object.defineProperty(record, 'content', { value: 'text', enumerable: false });
assert.equal(partitionEvidence([record]).notes[0].content, 'text', 'copied record must retain required content');
