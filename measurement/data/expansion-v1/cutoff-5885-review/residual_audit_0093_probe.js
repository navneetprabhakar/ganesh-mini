const assert = require('node:assert/strict');
const { compileAuditPacket } = require('./solution');
const component = () => ({exportData() {return {};}});
assert.throws(() => compileAuditPacket({actor:component(),evidence:component(),policy:component(),display:component(),extra:true}), TypeError);
