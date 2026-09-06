import { GapValue, expandGaps } from './solution';
let caught: unknown;
try { expandGaps({ outerGap: [1] as unknown as GapValue }); } catch (error) { caught = error; }
if (!(caught instanceof RangeError)) throw new Error('Array shorthand must have two or four members, not one');
