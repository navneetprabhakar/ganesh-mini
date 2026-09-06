import { coalesceSpans, type IntegerSpan } from './solution';
let rejected = false;
try { coalesceSpans(new Array<IntegerSpan>(1)); }
catch (error) { rejected = error instanceof RangeError; }
if (!rejected) throw new Error('Missing span must throw RangeError');
