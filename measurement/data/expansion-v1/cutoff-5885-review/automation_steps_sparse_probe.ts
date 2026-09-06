import { compilePlan } from './solution';
let caught = false;
try { compilePlan({actor:'A', mode:'safe', retries:0, steps:new Array<string>(1)}); }
catch (error) { if (!(error instanceof Error)) throw error; caught = true; }
if (!caught) throw new Error('Malformed missing step must be rejected');
