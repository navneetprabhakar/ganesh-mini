import { transitionIntake } from './solution';
const parcel = Object.defineProperty({ sender: 'A' }, 'id', { value: 'P', enumerable: false }) as { id: string; sender: string };
const result = transitionIntake({ status: 'waiting' }, { type: 'ARRIVE', parcel });
if (result.status !== 'reviewing' || result.parcel.id !== 'P') throw new Error('Validated parcel id lost during arrival copy');
