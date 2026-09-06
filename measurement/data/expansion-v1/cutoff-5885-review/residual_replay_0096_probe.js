const assert = require('node:assert/strict');
const { replayAccessEvents } = require('./solution');
const result = replayAccessEvents([{type:'ALLOW',principal:' alice ',scope:' read '}]);
assert.equal(result.principal, ' alice ', 'event values must be stored as supplied; no trimming requested');
