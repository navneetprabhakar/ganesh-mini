import { Material, Container, updateContainerValue } from './solution';
const a = new Material('a', 'A', Number.MAX_VALUE);
const b = new Material('b', 'B', 0);
const c = new Container('c', 'C', a, b, 2, 0, 0);
let rejected = false;
try { updateContainerValue(c, a, b); } catch (error) { if (error instanceof RangeError) rejected = true; else throw error; }
if (!rejected) throw new Error('all numeric values must remain finite; stored total=' + c.totalValue);
