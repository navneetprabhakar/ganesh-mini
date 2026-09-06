import {selectStorageBin} from './solution';
let rejected = false;
let result: number | undefined;
try {result = selectStorageBin([], new Array<number>(1));}
catch(error) {if (!(error instanceof RangeError)) throw error; rejected=true;}
console.log('rejected',rejected,'result',result);
if (!rejected) throw new Error('malformed preferred entry returned instead of RangeError');
