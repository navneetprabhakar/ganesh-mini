import { EntryBook } from './solution';
const book = new EntryBook();
for (const id of ['a', 'b', 'c']) book.add({ id, weight: 1 });
book.select('c');
if (book.move(Number.MAX_SAFE_INTEGER)?.id !== 'a') throw new Error('Safe integer offset must wrap without losing selected origin');
