'use strict';
const assert = require('node:assert/strict');
const { selectModules } = require('./solution');
// Even an unreachable module must have valid imports under whole-graph validation.
assert.throws(() => selectModules({unused: {imports: new Array(1), sideEffect: false}}, []), TypeError);
