import { createStandardCodecBank } from './solution';
let rejected = false;
try { createStandardCodecBank().encode('string-list', new Array<string>(1)); }
catch (e) { if (!(e instanceof RangeError)) throw e; rejected = true; }
if (!rejected) throw new Error('missing string member serialized as null');
