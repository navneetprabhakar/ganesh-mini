import { createReservationLine, withReservationQuantity } from './solution';
const line = createReservationLine('sku', 'Label', 1, 1);
Object.defineProperty(line, 'sku', { value: 'sku', enumerable: false });
if (withReservationQuantity(line, 2).sku !== 'sku') throw new Error('Quantity update must retain required SKU');
