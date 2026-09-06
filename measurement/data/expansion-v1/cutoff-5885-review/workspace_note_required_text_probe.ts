import { Note, createWorkspaceState, reduceWorkspace } from './solution';
const note: Note = { boardId: 'b', id: 'n', text: 'Text' };
Object.defineProperty(note, 'text', { value: 'Text', enumerable: false });
if (reduceWorkspace(createWorkspaceState(), { type: 'ReplaceNotes', notes: [note] }).notes[0].text !== 'Text') throw new Error('Required note text must survive replacement copying');
