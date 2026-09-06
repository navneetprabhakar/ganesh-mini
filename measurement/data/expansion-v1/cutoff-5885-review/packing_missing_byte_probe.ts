import { executePacking } from './solution';
let rejected = false;
try {
  executePacking({command:'pack', attachment:{kind:'text', name:'x', bytes:new Array<number>(1)}}, false);
} catch (error) {
  if (!(error instanceof RangeError)) throw error;
  rejected = true;
}
if (!rejected) throw new Error('Missing byte accepted instead of RangeError');
