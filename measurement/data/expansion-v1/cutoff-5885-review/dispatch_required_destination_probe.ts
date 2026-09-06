import { selectDispatches } from './solution';
const record = { id: 1, operator: 'A', destination: 'North', priority: 1 };
Object.defineProperty(record, 'destination', { value: 'North', enumerable: false });
if (selectDispatches([record], 'A')[0].destination !== 'North') throw new Error('Required destination lost');
