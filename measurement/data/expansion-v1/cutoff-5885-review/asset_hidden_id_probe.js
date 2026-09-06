'use strict';
const assert = require('node:assert/strict');
const { reviseAsset } = require('./solution');
const patch = Object.defineProperty({}, 'assetId', {value: 'changed', enumerable: false});
assert.throws(() => reviseAsset({assetId: 'a', label: 'L', category: 'C', active: true}, patch), TypeError);
