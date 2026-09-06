import { Polynomial } from './solution';
let threw = false;
try { new Polynomial(new Array<number>(1)); } catch { threw = true; }
if (!threw) throw new Error('Missing coefficient is not a finite numeric coefficient');
