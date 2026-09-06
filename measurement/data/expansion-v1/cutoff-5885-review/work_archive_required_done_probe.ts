import { WorkArchive } from './solution';
const item = { id: 1, title: 'Alpha', done: false };
Object.defineProperty(item, 'done', { value: false, enumerable: false });
const archive = new WorkArchive();
archive.add(item);
if (archive.find(1)?.done !== false) throw new Error('Required done flag lost');
