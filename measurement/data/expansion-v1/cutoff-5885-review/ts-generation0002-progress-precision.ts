import { ChunkTransferQueue } from './solution';

const chunk = 4503599627370497;
const queue = new ChunkTransferQueue([{ id: 'file', size: 18014398509481984 }], chunk, 1);
for (let count = 0; count < 3; count++) {
  const jobs = queue.nextBatch();
  if (jobs.length !== 1 || jobs[0].length !== chunk) throw new Error('unexpected job');
  queue.completeChunk('file', jobs[0].length);
}
const accepted = queue.snapshot()[0].accepted;
const expected = BigInt(chunk) * 3n;
if (BigInt(accepted) !== expected) {
  throw new Error(`accepted byte count ${accepted} differs from exact ${expected}`);
}
