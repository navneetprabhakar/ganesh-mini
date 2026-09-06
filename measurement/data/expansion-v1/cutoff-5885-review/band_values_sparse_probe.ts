import { makeBandMatrix } from "./solution";
let rejected = false;
try { makeBandMatrix(new Array<number>(1), 0); }
catch (error) { if (!(error instanceof TypeError)) throw error; rejected = true; }
if (!rejected) throw new Error("Missing finite band value bypassed validation");
