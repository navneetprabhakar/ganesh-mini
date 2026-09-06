import { SupplyLot, SupplyLotInput } from './solution';
const input: SupplyLotInput = { code: 'L1', description: 'Lot', quantity: 1, labels: [] };
Object.defineProperty(input, 'code', { enumerable: false });
const lot = new SupplyLot(input);
if (lot.details().code !== 'L1') throw new Error('Defensive copy must preserve required code');
