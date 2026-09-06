const assert = require('node:assert/strict');
const { applyPatchSet } = require('./solution');
const catalog = {};
Object.defineProperty(catalog, 'hidden', {value:{label:'Hidden',score:1}, enumerable:false});
const result = applyPatchSet(catalog, []);
assert.equal(Object.hasOwn(result, 'hidden'), true, 'own catalog record silently omitted; own versus enumerable domain needs disposition');
