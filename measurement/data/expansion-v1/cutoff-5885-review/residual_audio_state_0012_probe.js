'use strict';
const assert = require('node:assert/strict');
const { reduceAudioSession } = require('./solution');
const state = Object.create({route: '/', trackId: 't', playing: true, position: 2, caption: 'hello'});
const result = reduceAudioSession(state, {type: 'ROUTE_CHANGED', route: '/library'});
assert.equal(result.playing, true);
assert.equal(result.trackId, 't');
