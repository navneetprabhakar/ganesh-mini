import { DeviceCatalog, Device, DeviceKind, DeviceState } from './solution';
const device: Device = { id: 'd1', ownerCode: 'owner', label: 'Device', kind: DeviceKind.Sensor, state: DeviceState.Ready, unitCost: 1, ports: 0 };
Object.defineProperty(device, 'ownerCode', { enumerable: false });
const catalog = new DeviceCatalog();
catalog.add(device);
if (catalog.find('d1')?.ownerCode !== 'owner') throw new Error('Device copy must preserve required ownerCode');
