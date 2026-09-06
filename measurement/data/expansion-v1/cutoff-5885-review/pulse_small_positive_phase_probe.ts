import { pulseScale } from './solution';
const phase = 2 ** -52;
const expected = 0.5 + phase * 0.5;
if (pulseScale(phase) !== expected) throw new Error('representable triangular-wave increment erased');
