'use strict';
const assert = require('node:assert/strict');
const { markKeywords } = require('./solution');
assert.deepEqual(markKeywords('İx', ['x']), [{text: 'İ', matched: false}, {text: 'x', matched: true}]);
