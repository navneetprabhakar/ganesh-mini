import { Parcel, ParcelRegistry } from './solution';
const parcel: Parcel = { trackingId: 't', destination: 'Delhi', recipient: 'Alice' };
Object.defineProperty(parcel, 'destination', { value: 'Delhi', enumerable: false });
const registry = new ParcelRegistry();
registry.addParcel(parcel);
const found = registry.searchDestination('delhi');
if (found.length !== 1 || found[0].destination !== 'Delhi') throw new Error('Required destination must survive copying');
