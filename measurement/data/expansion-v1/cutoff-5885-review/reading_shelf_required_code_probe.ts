import { ReadingShelf, ShelfEntry } from './solution';
const entry: ShelfEntry = { code: 'A', caption: 'Caption' };
Object.defineProperty(entry, 'code', { enumerable: false });
const shelf = new ReadingShelf('Name', '', '', [entry], 'owner');
if (shelf.snapshot().entries[0].code !== 'A') throw new Error('required entry code lost');
