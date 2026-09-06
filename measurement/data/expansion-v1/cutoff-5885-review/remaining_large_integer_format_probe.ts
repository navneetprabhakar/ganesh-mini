import {formatRemaining} from './solution';
const seconds=1e25;
const exact=BigInt(seconds);
const expected=[exact/3600n,(exact/60n)%60n,exact%60n].map(v=>String(v).padStart(2,'0')).join(':');
if(formatRemaining(seconds)!==expected) throw new Error(`Large integer duration: expected ${expected}, got ${formatRemaining(seconds)}`);
