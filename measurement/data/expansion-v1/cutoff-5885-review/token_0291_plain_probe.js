const { advanceToken } = require('./solution');
class State { constructor() { Object.assign(this, { width: 2, height: 2, x: 0, y: 0, dx: 1, dy: 1 }); } }
let caught; try { advanceToken(new State()); } catch (e) { caught = e; }
if (!(caught instanceof TypeError)) throw new Error('Class instance accepted despite plain state requirement');
