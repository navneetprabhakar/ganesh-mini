const {PlaylistCursor} = require('./solution');
require('node:assert').throws(() => new PlaylistCursor(new Array(1), () => {}), TypeError);
