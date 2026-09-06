import { formatReading, DisplayScale } from './solution';
const actual = formatReading(1e21, DisplayScale.Length);
if (actual !== '1000000000000000000000.00 km') throw new Error('fixed decimal places lost: ' + actual);
