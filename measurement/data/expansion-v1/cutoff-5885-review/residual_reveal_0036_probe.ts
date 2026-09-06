import { revealCells } from './solution';
const result = revealCells([false], 1, 1, 1e200, 0, 1e199);
if (result[0] !== false) throw new Error('cell outside finite radius revealed because both squared values overflow to Infinity');
