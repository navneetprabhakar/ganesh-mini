import { WorkspaceStore, type Snapshot } from "./solution";
const store = new WorkspaceStore();
const value: Snapshot = JSON.parse('{"__proto__":1}');
store.put("draft", "key", value);
const restored = store.get("draft", "key") as Record<string, Snapshot>;
if (!Object.prototype.hasOwnProperty.call(restored, "__proto__") || restored.__proto__ !== 1) {
  throw new Error("Valid JSON object key __proto__ lost in clone");
}
