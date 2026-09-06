import { reduceAccessState, type AccessState } from './solution';
const state: AccessState = {phase:'editing',account:'a',secret:'s',error:null};
Object.defineProperty(state, 'phase', {enumerable:false});
const output = reduceAccessState(state, {type:'changeAccount',value:'b'});
if (output.phase !== 'editing') throw new Error('valid typed state loses non-enumerable discriminant');
