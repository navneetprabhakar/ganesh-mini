import { Blend, calculateBlendCost } from './solution';
const blend: Blend = { key: 'b', materialA: 'a', materialB: 'b', quantityA: 2, quantityB: 3, totalCost: 0 };
Object.defineProperty(blend, 'quantityA', { value: 2, enumerable: false });
const result = calculateBlendCost(blend, { key: 'a', label: 'A', unitCost: 4 }, { key: 'b', label: 'B', unitCost: 5 });
if (result.quantityA !== 2 || result.totalCost !== 23) throw new Error('Calculated blend must preserve required quantity');
