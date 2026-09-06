const { assignBins } = require('./solution');
class Item { constructor() { this.id = 'a'; this.units = 1; } }
let caught; try { assignBins([new Item()], [2]); } catch (e) { caught = e; }
if (!(caught instanceof TypeError)) throw new Error('Class instance accepted despite plain item requirement');
