import { CellCanvas } from './solution';
const canvas = new CellCanvas(5, 1);
canvas.fillColumns(['A', 'B']);
if (JSON.stringify(canvas.snapshot()) !== '[["A","A","A","B","B"]]') throw new Error('Column mapping must use floor, not round');
