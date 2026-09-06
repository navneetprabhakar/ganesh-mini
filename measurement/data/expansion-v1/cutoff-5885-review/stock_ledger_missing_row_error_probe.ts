import { StockLedger, type StockRow } from './solution';
let caught: unknown;
try { new StockLedger(new Array<StockRow>(1)); } catch (error) { caught = error; }
if (!(caught instanceof RangeError)) throw new Error('Malformed stock row must throw RangeError, got ' + String(caught));
