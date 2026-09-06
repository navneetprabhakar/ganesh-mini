import { LineDraft, InvoiceBook } from './solution';
const draft: LineDraft = { code: 'a', description: 'A', unitCents: 100, units: 2, rebateCentsPerUnit: 0 };
Object.defineProperty(draft, 'units', { value: 2, enumerable: false });
const book = new InvoiceBook(); book.begin(draft); book.save();
if (book.totals().subtotalCents !== 200) throw new Error('Required units must survive copying and preserve subtotal');
