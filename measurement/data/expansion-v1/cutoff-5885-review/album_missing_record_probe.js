'use strict';
const assert = require('node:assert/strict');
const { buildAlbumView } = require('./solution');
assert.throws(() => buildAlbumView(new Array(1)), TypeError);
