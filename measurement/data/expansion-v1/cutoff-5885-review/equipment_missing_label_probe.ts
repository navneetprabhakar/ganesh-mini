import { EquipmentCatalog } from './solution';
let rejected = false;
try { new EquipmentCatalog('key').add('key', { name: 'Pump', zone: 'West', labels: new Array<string>(1) }); }
catch { rejected = true; }
if (!rejected) throw new Error('Missing string label must be rejected');
