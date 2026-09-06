import { RGB, gradeVoxels } from './solution';
let caught: unknown;
try { gradeVoxels({ width: 1, height: 1, depth: 1, colors: new Array<RGB>(1) }, { gain: { r: 1, g: 1, b: 1 }, offset: { r: 0, g: 0, b: 0 } }); } catch (error) { caught = error; }
if (!(caught instanceof RangeError)) throw new Error('Missing color must fail finite-channel validation');
