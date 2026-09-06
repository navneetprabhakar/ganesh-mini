import { Reservation, withdrawReservation } from './solution';
const reservation: Reservation = { id: 'r', guest: 'Alice' };
Object.defineProperty(reservation, 'guest', { value: 'Alice', enumerable: false });
if (withdrawReservation([reservation], 'r').removed.guest !== 'Alice') throw new Error('Removed reservation must preserve required guest');
