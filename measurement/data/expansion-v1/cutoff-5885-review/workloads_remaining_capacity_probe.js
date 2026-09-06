'use strict';
const assert = require('node:assert/strict');
const { assignWorkloads } = require('./solution');
assert.deepEqual(assignWorkloads([{ id: 'w', capacity: 2 }], [{ id: 'a', units: 1 }, { id: 'b', units: 1 }]).assignments, [
  { jobId: 'a', workerId: 'w', units: 1 }, { jobId: 'b', workerId: 'w', units: 1 }
]);
