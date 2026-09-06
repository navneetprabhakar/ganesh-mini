import { Shipment, queueAll } from './solution';
const shipment: Shipment = { code: 'A', description: 'Alpha', stage: 'sent', feeCents: 0 };
Object.defineProperty(shipment, 'code', { value: 'A', enumerable: false });
if (queueAll([shipment])[0].code !== 'A') throw new Error('Bulk stage change must preserve required code');
