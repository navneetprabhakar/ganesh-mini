import { composeDocument } from "./solution";
let rejected = false;
try { composeDocument({top: new Array<string>(1), bottom: []}, []); }
catch (error) { if (!(error instanceof TypeError)) throw error; rejected = true; }
if (!rejected) throw new Error("Sparse chrome top bypassed string-only validation");
