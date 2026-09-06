const { makeDensityGrid } = require('./solution');
class Options { constructor() { this.radius = 0; this.cap = 1; } }
let caught; try { makeDensityGrid([], 1, 1, new Options()); } catch (error) { caught = error; }
if (!(caught instanceof TypeError || caught instanceof RangeError)) throw new Error('Class options accepted despite plain-object requirement');
