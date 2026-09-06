'use strict';
const assert = require('node:assert/strict');
const { createSignalHub } = require('./solution');
const hub = createSignalHub();
assert.throws(() => hub.on('topic'), TypeError);
assert.throws(() => hub.off('topic', undefined), TypeError);
