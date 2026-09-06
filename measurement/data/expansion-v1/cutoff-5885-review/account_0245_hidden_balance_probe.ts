import { MemoryAccountBook } from './solution';
const initial = Object.defineProperty({}, 'alice', { value: 5n, enumerable: false });
const book = new MemoryAccountBook(initial);
if (book.balanceOf('alice') !== 5n) throw new Error('Own initial balance lost despite constructor copy requirement');
