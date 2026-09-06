import { DimensionLedger, type Dimensions } from "./solution";
const initial: Dimensions = {width: 2, height: 3};
Object.defineProperty(initial, "width", {enumerable: false});
const ledger = new DimensionLedger(initial);
if (ledger.current().width !== 2) throw new Error("Valid required width lost in dimension snapshot");
