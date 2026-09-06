import { buildDetailDialog } from './solution';
let rejected = false;
try { buildDetailDialog({ title: 'T', banner: 'B', owner: 'O', section: 'S', published: 'P', paragraphs: [], images: new Array<string>(1) }); }
catch (e) { if (!(e instanceof TypeError)) throw e; rejected = true; }
if (!rejected) throw new Error('missing nonblank image accepted');
