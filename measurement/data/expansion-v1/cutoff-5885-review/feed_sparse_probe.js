'use strict';
const assert = require('node:assert/strict');
const { FeedMapper } = require('./solution');
const mapper = new FeedMapper(true);
const packet = {kind: 'samples', data: new Array(1)};
assert.equal(mapper.canHandle(packet), false);
assert.throws(() => [...mapper.map(packet, 0)], TypeError);
