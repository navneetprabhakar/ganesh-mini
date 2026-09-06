import { partitionLedger, LedgerEntry } from './solution';
const entry: LedgerEntry = { id: 'a', asset: ' USD ', amount: 1 };
Object.defineProperty(entry, 'asset', { value: ' USD ', enumerable: false });
const result = partitionLedger([entry], 'USD', 'EUR');
if (result.primary[0].asset !== entry.asset) throw new Error('Validated original asset string lost: ' + JSON.stringify(result));
