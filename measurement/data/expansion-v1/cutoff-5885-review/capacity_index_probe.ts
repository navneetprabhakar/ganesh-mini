import { RegionalCapacityLedger } from './solution';
const ledger = new RegionalCapacityLedger();
ledger.setSite({ used: 1, limit: 2 }, 4294967295);
if (ledger.used !== 1 || ledger.limit !== 2 || ledger.meanUtilization !== 0.5) {
  throw new Error('Accepted nonnegative integer slot omitted from totals: ' + JSON.stringify({used: ledger.used, limit: ledger.limit, mean: ledger.meanUtilization}));
}
