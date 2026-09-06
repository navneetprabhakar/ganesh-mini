import { buildSectionRows } from "./solution";

const item = { sku: "x", label: "X", metadata: { value: 1 } };
const rows = buildSectionRows({ Section: [item] }, false);
const returned = rows[0].items[0] as typeof item;
returned.metadata.value = 2;
if (item.metadata.value !== 1) throw new Error("Deep-copy promise violated by retained nested property");
