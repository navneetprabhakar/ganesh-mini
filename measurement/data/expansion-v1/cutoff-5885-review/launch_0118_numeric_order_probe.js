'use strict';
const assert = require('node:assert/strict');
const { parseLaunchLink } = require('./solution');
assert.deepEqual(Object.keys(parseLaunchLink('desk://run/go?2=b&1=a').parameters), ['2', '1'], 'query keys must preserve source order');
