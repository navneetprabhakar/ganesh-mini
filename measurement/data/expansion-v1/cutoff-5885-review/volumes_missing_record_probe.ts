import { Volume, filterVolumes } from './solution';
let caught: unknown;
try { filterVolumes(new Array<Volume>(1), ''); } catch (error) { caught = error; }
if (!(caught instanceof RangeError)) throw new Error('Missing volume must reject malformed input');
