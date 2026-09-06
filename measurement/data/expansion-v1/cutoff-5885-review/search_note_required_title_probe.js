'use strict';
const assert = require('node:assert/strict');
const { searchNotes } = require('./solution');
const note = { title: 'Title', body: 'Body' };
Object.defineProperty(note, 'title', { enumerable: false });
assert.equal(searchNotes([note], 'title')[0].title, 'Title');
