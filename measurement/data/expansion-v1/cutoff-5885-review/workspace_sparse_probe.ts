import { WorkspaceStore, type Snapshot } from "./solution";
let rejected = false;
try { new WorkspaceStore().put("draft", "key", new Array<Snapshot>(1)); }
catch (error) { if (!(error instanceof TypeError)) throw error; rejected = true; }
if (!rejected) throw new Error("Undefined array slot bypassed JSON-like snapshot validation");
