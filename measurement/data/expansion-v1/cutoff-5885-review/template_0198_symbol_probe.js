const assert = require('node:assert/strict');
const { renderTemplate } = require('./solution');
assert.throws(() => renderTemplate('', { [Symbol('bad')]: 42 }), TypeError,
  'Every own enumerable key/value must be validated; symbol key and numeric value are invalid');
