import { SequenceChooser } from './solution';
let rejected = false;
try { new SequenceChooser({kind: 'choice', options: new Array<string>(1)}); }
catch { rejected = true; }
if (!rejected) throw new Error('sparse choices accepted although options must be nonempty strings');
