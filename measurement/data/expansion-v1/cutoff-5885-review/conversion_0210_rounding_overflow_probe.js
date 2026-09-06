const assert = require('node:assert/strict');
const buildConversionView = require('./solution');
assert.throws(() => buildConversionView({ estimatedRate: Number.MAX_VALUE, amount: 1,
  source: 'A', target: 'B', direction: 'forward' }), TypeError,
  'Required precision conversion overflows but no TypeError is thrown');
