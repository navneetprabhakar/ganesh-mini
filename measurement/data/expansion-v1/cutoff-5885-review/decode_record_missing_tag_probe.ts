import { decodeRecord } from './solution';
let rejected = false;
try { decodeRecord('full', { key: '', label: '', tags: new Array(1) }); }
catch (e) { if (!(e instanceof TypeError) || e.message !== 'Malformed record') throw e; rejected = true; }
if (!rejected) throw new Error('missing string tag accepted');
