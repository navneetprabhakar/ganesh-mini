import { createStatusPanel } from './solution';
let rejected = false;
try { createStatusPanel({ kind: 'status', values: new Array<number>(1) }); }
catch (error) { rejected = error instanceof TypeError; }
if (!rejected) throw new Error('Missing finite numeric value must throw TypeError');
