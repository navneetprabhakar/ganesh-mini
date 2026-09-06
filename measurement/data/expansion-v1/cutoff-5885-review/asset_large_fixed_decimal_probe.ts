import { buildAssetRegister } from './solution';
const result = buildAssetRegister([{ code: 'a', label: 'A', cost: 1e21 }]);
if (result.lines[0] !== 'a|A|1000000000000000000000.00') throw new Error('Finite cost must have exactly two decimal places');
