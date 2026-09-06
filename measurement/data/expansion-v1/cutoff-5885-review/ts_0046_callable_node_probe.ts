import { makeNode } from "./solution";

const node = Object.assign(() => undefined, { tag: "section" });
let calls = 0;
const returned = makeNode((tag) => {
  calls++;
  if (tag !== "section") throw new Error("Wrong factory argument");
  return node;
});
if (returned !== node || calls !== 1) throw new Error("Node identity/call count changed");
