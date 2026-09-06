import { QueueMemo, createMemoQueue } from './solution';
let threw = false;
try { createMemoQueue(new Array<QueueMemo>(1)); } catch { threw = true; }
if (!threw) throw new Error('Missing memo must not bypass required ID/title/priority validation');
