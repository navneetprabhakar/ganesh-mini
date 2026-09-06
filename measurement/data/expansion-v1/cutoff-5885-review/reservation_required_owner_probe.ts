import { Reservation, ReservationStore } from './solution';
const reservation: Reservation = { id: 'r', owner: 'alice', seats: 1, status: 'held' };
Object.defineProperty(reservation, 'owner', { value: 'alice', enumerable: false });
const records = new ReservationStore([reservation]).listByOwner('alice');
if (records.length !== 1 || records[0].owner !== 'alice') throw new Error('Required owner must survive input copying');
