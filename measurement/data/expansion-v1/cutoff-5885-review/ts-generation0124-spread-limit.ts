import { QueueWeaveCommand } from './solution';

const tracks = Array.from({ length: 200000 }, (_, i) => String(i));
const original = tracks;
const result = new QueueWeaveCommand().run({ canReorder: true, tracks });
if (tracks !== original || result === tracks || result.length !== 200000 ||
    result[0] !== '0' || result[99999] !== '199998' || result[100000] !== '1') {
  throw new Error('weave result or ownership mismatch');
}
