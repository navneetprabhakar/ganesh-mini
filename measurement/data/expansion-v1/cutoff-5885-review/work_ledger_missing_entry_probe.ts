import { WorkEntry, WorkLedger } from './solution';
let caught: unknown;
try { new WorkLedger(new Array<WorkEntry>(1)); } catch (error) { caught = error; }
if (!(caught instanceof TypeError)) throw new Error('Missing work entry must reject malformed input');
