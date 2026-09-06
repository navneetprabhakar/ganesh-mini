'use strict';
const assert = require('node:assert/strict');
const { TripLedger } = require('./solution');
assert.throws(() => new TripLedger([{ id: 'w', mode: 'walk', distanceKm: 1, durationMinutes: 1, stepRate: 1, points: new Array(1) }]), TypeError);
