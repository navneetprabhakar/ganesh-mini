import { StockLedger } from "./solution";
const ledger = new StockLedger([
  {sku: "A", quantity: Number.MAX_SAFE_INTEGER, reason: "receive"},
  {sku: "A", quantity: 2, reason: "receive"},
  {sku: "A", quantity: -Number.MAX_SAFE_INTEGER, reason: "remove"}
]);
if (ledger.balanceFor("A") !== 2) throw new Error("Safe integer changes must sum to exact representable balance 2");
