import { createLedgerReport, type LedgerEntry } from './solution';
const entry: LedgerEntry = {id:'X', account:'A', day:0, delta:1};
Object.defineProperty(entry, 'id', {enumerable:false});
if (createLedgerReport('A', 0, 0, [entry]).entries[0].id !== 'X') throw new Error('Required ledger ID lost');
