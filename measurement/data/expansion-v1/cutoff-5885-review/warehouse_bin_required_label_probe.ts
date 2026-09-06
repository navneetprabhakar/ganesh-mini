import { initialWarehouseState, reduceWarehouse, BinRecord } from './solution';
const bin: BinRecord = { code: 'a', label: 'Alpha', enabled: false };
Object.defineProperty(bin, 'label', { enumerable: false });
const result = reduceWarehouse(initialWarehouseState, { type: 'REGISTER_BIN', bin });
if (result.bins[0].label !== 'Alpha') throw new Error('Registered bin must preserve required label');
