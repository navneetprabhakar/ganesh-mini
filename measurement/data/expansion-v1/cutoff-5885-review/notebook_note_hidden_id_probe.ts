import { NotebookIndex, type Note } from './solution';
const note: Note = {id:'n', folderId:'f', body:'body'};
Object.defineProperty(note, 'id', {enumerable:false});
const index = new NotebookIndex();
index.addFolder({id:'f', label:'Folder', notes:[note]});
if (index.notesIn('f')[0].id !== 'n') throw new Error('Required note ID lost during defensive copy');
