import { EntityKey, NoteSnapshot, NoteRevisedRecord } from './solution';
const note: NoteSnapshot = { key: new EntityKey('n1'), body: 'before', revision: 0 };
Object.defineProperty(note, 'body', { enumerable: false });
const event = new NoteRevisedRecord(0, note, { body: 'after' });
if (event.note.body !== 'before') throw new Error('Event snapshot must preserve required body');
