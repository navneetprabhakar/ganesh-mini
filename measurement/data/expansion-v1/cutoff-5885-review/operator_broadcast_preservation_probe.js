'use strict';
const assert = require('node:assert/strict');
const disableOperatorPreview = require('./solution');
const operator = { previewEnabled: true, broadcastEnabled: true };
Object.defineProperty(operator, 'broadcastEnabled', { enumerable: false });
const result = disableOperatorPreview({ operator, viewers: [] });
assert.equal(result.operator.broadcastEnabled, true);
