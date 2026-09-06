const {resolvePass} = require('./solution');
require('node:assert').throws(() => resolvePass([{memberId:'m',passes:new Array(1)}], 'bad', () => ({memberId:'m'})), TypeError);
