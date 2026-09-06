const assert = require('node:assert/strict');
const { configureStrip } = require('./solution');
const thresholds = {};
Object.defineProperty(thresholds, '10', { value: { visible: 2, gap: 3 }, enumerable: false });
assert.equal(configureStrip({ itemCount: 0, base: { visible: 1, gap: 0 }, thresholds }, 10).visible, 2,
  'Own threshold must participate even when non-enumerable');
