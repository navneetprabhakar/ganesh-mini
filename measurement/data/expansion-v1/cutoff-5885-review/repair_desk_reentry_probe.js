'use strict';
const assert = require('node:assert/strict');
const { createRepairDesk } = require('./solution');
let nested;
let entered = false;
const desk = createRepairDesk(() => {
  if (!entered) {
    entered = true;
    nested = desk.open('Nested issue', 'Nested owner');
  }
});
const outer = desk.open('Outer issue', 'Outer owner');
assert.notEqual(outer.ticketId, nested.ticketId, 'Successful opens must not share an ID');
assert.equal(desk.list('all').length, 2, 'Both successfully opened tickets must remain');
