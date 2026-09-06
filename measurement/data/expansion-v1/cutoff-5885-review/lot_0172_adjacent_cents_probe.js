'use strict';
const assert = require('node:assert/strict');
const { createLotView } = require('./solution');
const cents = Number.MAX_SAFE_INTEGER - 1;
const exact = BigInt(cents);
const expected = String(exact / 100n) + '.' + String(exact % 100n).padStart(2, '0');
const view = createLotView({ reserveCents: cents, ownerId: 'o', ownerName: 'Owner', eventDate: '2026-01-01', startTime: '00:00' }, { id: 'v' }, null, () => {});
assert.equal(view.price, expected, 'safe integer cents must format exactly');
