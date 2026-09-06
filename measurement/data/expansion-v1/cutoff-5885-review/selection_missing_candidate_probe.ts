import { SelectionLedger } from './solution';
const ledger = new SelectionLedger();
ledger.replace(['old']);
let caught: unknown;
try { ledger.replace(new Array<string>(1)); } catch (error) { caught = error; }
if (!(caught instanceof TypeError)) throw new Error('Missing candidate must reject malformed input');
if (ledger.values().join(',') !== 'old') throw new Error('Malformed replacement must be atomic');
