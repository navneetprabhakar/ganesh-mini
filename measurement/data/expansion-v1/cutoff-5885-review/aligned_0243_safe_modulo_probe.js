const { lastAligned } = require('./solution');
const result = lastAligned(0, Number.MAX_SAFE_INTEGER - 1, Number.MAX_SAFE_INTEGER);
if (result !== 0) throw new Error('Safe interval returned nonmultiple after remainder normalization overflow: ' + result);
