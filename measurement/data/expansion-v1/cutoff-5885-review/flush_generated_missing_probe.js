const {flushJobs} = require('./solution');
require('node:assert').throws(() => flushJobs(['root'], () => new Array(1), 1), TypeError);
