import { applyServiceReply, type ClientState } from './solution';
const state = {screen:'checkout', alert:'old'} as ClientState;
Object.defineProperty(state, 'token', {value:'retained', enumerable:false});
const result = applyServiceReply(state, {status:500, message:'retry'});
console.log('token', result.token);
if (result.token !== 'retained') throw new Error('unchanged token lost');
