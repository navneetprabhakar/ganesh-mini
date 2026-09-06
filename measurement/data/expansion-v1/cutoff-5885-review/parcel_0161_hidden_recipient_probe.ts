import { ParcelLedger, type Parcel } from './solution';
const parcel: Parcel = { id: 'p', recipient: 'A', units: 1, massKg: 1 };
Object.defineProperty(parcel, 'recipient', { value: 'A', enumerable: false });
const ledger = new ParcelLedger([parcel]);
if (ledger.get('p').recipient !== 'A') throw new Error('validated recipient lost in stored parcel');
