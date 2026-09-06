import {ChannelHub} from './solution';
const values: number[] = [];
const length: number = values.push(1);
if (length !== 1 || new ChannelHub<number>().publish('x', 1) !== 0) throw new Error('unexpected result');
