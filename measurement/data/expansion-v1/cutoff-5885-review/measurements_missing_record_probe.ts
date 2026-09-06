import { Measurement, selectMeasurements } from './solution';
let caught: unknown;
try { selectMeasurements(new Array<Measurement>(1), { limit: 1, offset: 0, sortBy: 'bytes', direction: 'asc' }); } catch (error) { caught = error; }
if (!(caught instanceof RangeError)) throw new Error('Missing measurement must not bypass validation');
