'use strict';
const assert = require('node:assert/strict');
const { selectParcelsByZone } = require('./solution');
const input = new Array(2);
const parcel = {zone: 'North'};
input[1] = parcel;
const result = selectParcelsByZone(input, 'north');
assert.deepEqual(result, [parcel]);
assert.equal(result[0], parcel);
