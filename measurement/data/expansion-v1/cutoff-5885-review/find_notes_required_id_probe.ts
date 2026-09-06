import { Note, findNotes } from './solution';
(async () => {
  const note: Note = { id: 'n', heading: 'Title', body: 'Body', categoryId: 'c' };
  Object.defineProperty(note, 'id', { enumerable: false });
  const found = await findNotes([note], '', async () => []);
  if (found[0].id !== 'n') throw new Error('required note id lost');
})();
