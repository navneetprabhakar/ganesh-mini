'use strict';
const assert = require('node:assert/strict');
const { prepareWorkshopRequest } = require('./solution');
const result = prepareWorkshopRequest({title: 'T', summary: 'S', host: 'H', contactEmail: 'a@b', secret: 'Abcdef1!', topics: new Array(1)});
assert.equal(result.ok, false);
assert.equal(result.payload, null);
