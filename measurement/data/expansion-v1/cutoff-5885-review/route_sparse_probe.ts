import { orderPatterns } from "./solution";
let rejected = false;
try { orderPatterns(new Array<string>(1)); }
catch (error) {
  if (!(error instanceof Error) || error.message !== "invalid pattern") throw error;
  rejected = true;
}
if (!rejected) throw new Error("Missing pattern bypassed required route validation");
