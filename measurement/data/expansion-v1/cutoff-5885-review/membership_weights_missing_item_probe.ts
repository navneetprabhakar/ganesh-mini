import { assignMembershipWeights, KeyedValue } from './solution';
let rejected = false;
try { assignMembershipWeights(new Array<KeyedValue<number>>(1), []); }
catch (e) { if (!(e instanceof TypeError)) throw e; rejected = true; }
if (!rejected) throw new Error('missing keyed item accepted');
