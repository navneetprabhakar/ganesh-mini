'use strict';
const assert = require('node:assert/strict');
const { normalizePreferences } = require('./solution');
const flags = JSON.parse('{"__proto__":true,"normal":false}');
const result = normalizePreferences({ flags });
assert.deepEqual(Object.keys(result.flags), ['__proto__', 'normal']);
assert.equal(result.flags.__proto__, true);
