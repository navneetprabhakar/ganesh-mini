import { blend } from './solution';
if (blend(-Number.MAX_VALUE, Number.MAX_VALUE, 0) !== -Number.MAX_VALUE) throw new Error('Zero fraction must return finite starting endpoint');
