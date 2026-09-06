const assert = require('node:assert/strict');
const { partitionAssetDirectives } = require('./solution');
const source = '#asset "a\u2028b"';
assert.deepEqual(partitionAssetDirectives(source), [{type:'text', value:source}]);
