import { mergeRosterPages } from './solution';
let rejected = false;
try { mergeRosterPages([{ page: 0, complete: true, entries: [{ id: 42 as unknown as string, displayName: 'Name' }] }]); }
catch (e) { if (!(e instanceof TypeError)) throw e; rejected = true; }
if (!rejected) throw new Error('non-string roster id accepted');
