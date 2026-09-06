import { BranchMetrics, StockRow } from "./solution";

const stocks = new Array<StockRow>(1);
const metrics = new BranchMetrics(() => stocks, () => [], () => []);
if (metrics.countDepleted(1) !== -1) {
  throw new Error("Sparse malformed stock provider was accepted as zero records");
}
