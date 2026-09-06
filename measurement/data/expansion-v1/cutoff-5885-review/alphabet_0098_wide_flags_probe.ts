import { alphabet } from './solution';
let rejected = false;
try { alphabet(2 ** 32 + 1); } catch (error) { if (error instanceof RangeError) rejected = true; else throw error; }
if (!rejected) throw new Error('unknown bit 32 was discarded instead of rejected');
