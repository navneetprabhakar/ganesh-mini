const assert = require('node:assert/strict');
const { calculateInvoiceSubtotal } = require('./solution');
assert.equal(calculateInvoiceSubtotal([{ unitPrice: Number.MAX_VALUE, quantity: 1 }]), Number.MAX_VALUE,
  'Finite integer subtotal should remain finite when rounded to two decimal places');
