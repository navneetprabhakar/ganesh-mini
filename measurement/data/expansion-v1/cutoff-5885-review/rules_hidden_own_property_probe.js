'use strict';
const assert = require('node:assert/strict');
const { serializeRules } = require('./solution');
const rules = {};
Object.defineProperty(rules, 'color', { value: 'red', enumerable: false });
assert.equal(serializeRules(rules), 'color:red');
