import { RecordShelf } from './solution';
let rejected = false;
try { new RecordShelf().add({ id: 1, label: 'Alpha', tags: new Array<string>(1) }); }
catch (error) { rejected = error instanceof TypeError; }
if (!rejected) throw new Error('Missing tag must throw TypeError');
