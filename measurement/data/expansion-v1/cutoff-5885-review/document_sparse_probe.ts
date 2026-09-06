import { DocumentSignal } from './solution';
const signal = new DocumentSignal({title: 'old', tags: ['original']});
let notified = false;
signal.subscribe(() => { notified = true; });
let rejected = false;
try { signal.replace({title: 'new', tags: new Array<string>(1)}); }
catch (error) { if (error instanceof TypeError) rejected = true; else throw error; }
if (!rejected || notified || signal.value.title !== 'old') throw new Error('sparse tags accepted and state changed/notified');
