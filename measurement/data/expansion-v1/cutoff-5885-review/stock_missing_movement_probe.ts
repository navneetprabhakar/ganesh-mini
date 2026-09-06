import { StockMovement, summarizeStock } from './solution';
let rejected = false;
try { summarizeStock('A', 0, 1, new Array<StockMovement>(1)); }
catch (e) { if (!(e instanceof RangeError)) throw e; rejected = true; }
if (!rejected) throw new Error('missing movement accepted');
