const { resolveBindings } = require('./solution');
let caught;
try { resolveBindings({}, [{ from: 'missing', imported: 'x', local: 'x' }, { from: 'm', imported: 'y', local: 'x' }]); }
catch (error) { caught = error; }
if (!(caught instanceof ReferenceError)) throw new Error('Later duplicate local error displaced first missing-module error: ' + (caught && caught.name));
