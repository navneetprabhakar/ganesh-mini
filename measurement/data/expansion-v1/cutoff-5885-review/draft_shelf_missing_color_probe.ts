import { DraftShelf } from './solution';
let rejected = false;
try { new DraftShelf().add({ name: 'Alpha', colors: new Array<string>(1) }); }
catch (error) { rejected = error instanceof TypeError; }
if (!rejected) throw new Error('Missing color must throw TypeError');
