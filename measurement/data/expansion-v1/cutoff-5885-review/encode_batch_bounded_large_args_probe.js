'use strict';
const assert = require('node:assert/strict');
const { encodeBatch } = require('./solution');
const values = new Array(150000).fill(1);
const result = encodeBatch(null, [{}], () => ({ command: 'run', args: values }));
assert.equal(result.args.length, values.length);
assert.notEqual(result.args, values);
