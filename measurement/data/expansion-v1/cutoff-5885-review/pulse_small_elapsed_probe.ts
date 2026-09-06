import { samplePulse } from './solution';
const elapsed = 2 ** -54;
const frame = samplePulse({ x: [0, 1], opacity: [0, 1, 0], scale: [1, 2, 1], duration: 1 }, elapsed);
if (frame.x !== elapsed) throw new Error('Small positive elapsed incorrectly treated as exact end: ' + frame.x);
