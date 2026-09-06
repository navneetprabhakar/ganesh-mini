import { averageBuckets } from "./solution";
let rejected = false;
try { averageBuckets(new Array<number>(1), 1); }
catch (error) { if (!(error instanceof TypeError)) throw error; rejected = true; }
if (!rejected) throw new Error("Missing numeric element bypassed finite-value validation");
