import { filterCharges } from './solution';
const records = filterCharges([], 'a', '0099-01-01', '0099-01-01');
if (records.length !== 0) throw new Error('Valid Gregorian year 0099 must accept empty charges');
