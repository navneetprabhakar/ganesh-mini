import { buildEntranceTimeline } from './solution';
const frames = buildEntranceTimeline(['a', 'b'], {step: 1e308, duration: 1e308, cycles: 1});
if (frames[0].start !== 0) throw new Error('first-cycle first-frame start is not zero: ' + frames[0].start);
