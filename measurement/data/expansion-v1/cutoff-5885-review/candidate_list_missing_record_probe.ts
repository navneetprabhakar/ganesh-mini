import { Candidate, CandidateList } from './solution';
let caught: unknown;
try { new CandidateList(new Array<Candidate>(1), () => {}); } catch (error) { caught = error; }
if (!(caught instanceof TypeError)) throw new Error('Missing candidate must be rejected at construction');
