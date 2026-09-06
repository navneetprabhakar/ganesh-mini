'use strict';
const assert = require('node:assert/strict');
const { createImageCabinet } = require('./solution');
assert.throws(() => createImageCabinet().add({id: 'a', mime: new String('image/png'), bytes: [1]}));
