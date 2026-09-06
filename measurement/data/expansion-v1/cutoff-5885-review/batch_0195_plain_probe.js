const { summarizeBatch } = require('./solution');
class Record { constructor() { this.batchId = 'b'; this.category = 'c'; this.quantity = 1; } }
let caught; try { summarizeBatch([new Record()], 'b'); } catch (e) { caught = e; }
if (!(caught instanceof TypeError)) throw new Error('Class instance accepted despite plain record requirement');
