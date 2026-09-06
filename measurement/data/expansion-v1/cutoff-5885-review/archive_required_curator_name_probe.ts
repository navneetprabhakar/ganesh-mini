import { ArchiveDirectory } from './solution';
const curator = { id: 'c', name: 'Ada' };
Object.defineProperty(curator, 'name', { value: 'Ada', enumerable: false });
const directory = new ArchiveDirectory([curator], [], [], []);
if (directory.findCurator('c')?.name !== 'Ada') throw new Error('Required curator name lost');
