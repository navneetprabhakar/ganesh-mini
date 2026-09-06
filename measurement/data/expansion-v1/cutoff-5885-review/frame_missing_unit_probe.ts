import { makeFrameValidator } from './solution';
const result = makeFrameValidator('data', 2)({ kind: 'data', units: new Array<number>(1) });
if (result.ok || result.reason !== 'malformed-unit') throw new Error('Missing unit must be malformed');
