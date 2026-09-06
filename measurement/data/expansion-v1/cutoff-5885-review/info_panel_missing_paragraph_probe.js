'use strict';
const assert = require('node:assert/strict');
const { renderInfoPanel } = require('./solution');
assert.throws(() => renderInfoPanel({ heading: 'H', paragraphs: new Array(1) }, { background: '#ffffff', text: '#000000', padding: 0 }), TypeError);
