const {listNotes} = require('./solution');
require('node:assert').throws(() => listNotes(new Array(1)), TypeError);
