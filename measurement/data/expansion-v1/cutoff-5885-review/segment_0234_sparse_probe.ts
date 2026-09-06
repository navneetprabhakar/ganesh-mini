import { SegmentBuffer } from './solution';
let caught: unknown;
try { SegmentBuffer.fromSnapshot({ length: 1, cells: new Array<string>(1) }); }
catch (error) { caught = error; }
if (!(caught instanceof TypeError)) throw new Error('Sparse snapshot accepted despite every-cell string validation requirement');
