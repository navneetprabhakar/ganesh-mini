'use strict';
const assert = require('node:assert/strict');
const { createLotView } = require('./solution');
const view = createLotView({ reserveCents: 1, ownerId: 'o', ownerName: 'Owner', eventDate: '0099-01-01', startTime: '00:00' }, { id: 'v' }, null, () => {});
assert.equal(view.schedule, '0099-01-01 00:00');
