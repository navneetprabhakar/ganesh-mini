import { labelsDueAt, type RecurrenceRule } from './solution';
let caught = false;
try { labelsDueAt(0, new Array<RecurrenceRule>(1)); }
catch (error) { if (!(error instanceof RangeError)) throw new Error('Malformed rule must throw RangeError'); caught = true; }
if (!caught) throw new Error('Malformed rule must be rejected');
