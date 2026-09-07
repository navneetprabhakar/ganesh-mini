import { BinaryRateLedger } from './solution';

const ledger = new BinaryRateLedger();
for (let i = 0; i < 200000; i++) ledger.add(i % 2, (i + 1) % 2);
const worst = ledger.worst();
if (ledger.size !== 200000 || worst === null || worst.falseAlarm !== 1 || worst.missedDetection !== 1) {
  throw new Error('independent worst rates or size mismatch');
}
