import { TurnOrder } from './solution';
const order = new TurnOrder(['a', 'b', 'c']);
order.rotate(2); order.rotate(Number.MAX_SAFE_INTEGER);
if (order.current() !== 'a') throw new Error('Safe integer rotation must not lose prior offset');
