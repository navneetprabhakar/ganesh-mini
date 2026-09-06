import { ReservationBook, StockItem } from './solution';
const line: StockItem = { sku: 'A', quantity: 1 };
Object.defineProperty(line, 'quantity', { enumerable: false });
const book = new ReservationBook([{ sku: 'A', quantity: 3 }]);
book.reserve('r', [line]);
const row = book.snapshot().stock[0];
if (row.available !== 2 || row.reserved !== 1) throw new Error('valid required quantity lost, corrupting stock');
