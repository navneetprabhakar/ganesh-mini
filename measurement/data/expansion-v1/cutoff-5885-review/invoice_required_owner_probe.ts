import { InvoiceRow, selectInvoicePage } from './solution';
const row: InvoiceRow = { number: '1', amountCents: 1, issuedDay: '2026-01-01', owner: 'Alice' };
Object.defineProperty(row, 'owner', { value: 'Alice', enumerable: false });
if (selectInvoicePage([row], {}).items[0].owner !== 'Alice') throw new Error('Invoice copy must preserve required owner');
