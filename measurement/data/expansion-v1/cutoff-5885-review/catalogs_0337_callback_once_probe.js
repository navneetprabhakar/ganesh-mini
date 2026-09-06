const { compareCatalogs } = require('./solution');
let calls = 0;
compareCatalogs([], [], () => { calls++; if (calls === 1) throw new Error('consumer failure'); });
setImmediate(() => { if (calls !== 1) throw new Error('Callback invoked more than once after consumer throw: ' + calls); });
