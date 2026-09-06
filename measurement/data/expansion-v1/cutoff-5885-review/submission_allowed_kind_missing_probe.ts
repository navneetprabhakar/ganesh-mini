import {SubmissionGate} from './solution';
let rejected=false;try { new SubmissionGate(1,1,new Array<string>(1)); } catch(e) { if(!(e instanceof TypeError)) throw e;rejected=true; }
if(!rejected) throw new Error('Missing allowed kind accepted');
