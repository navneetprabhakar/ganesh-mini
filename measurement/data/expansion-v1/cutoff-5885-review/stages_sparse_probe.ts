import { attachStages } from "./solution";
const stages: object[] = [];
let rejected = false;
try { attachStages({ stages }, new Array<object>(1)); }
catch (error) { if (!(error instanceof TypeError)) throw error; rejected = true; }
if (!rejected || stages.length !== 0) throw new Error("Missing stage accepted and host mutated instead of atomic TypeError");
