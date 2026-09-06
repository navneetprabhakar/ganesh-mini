import { summarizeSamples } from './solution';
const samples = Array.from({ length: 150000 }, (_, position) => ({ position, amount: 1 }));
const result = summarizeSamples(samples, 0, samples.length - 1);
if (result.count !== 150000 || result.total !== 150000 || result.minimum !== 1 || result.maximum !== 1) throw new Error('incorrect bounded sample summary');
