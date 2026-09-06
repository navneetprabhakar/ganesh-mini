import { composeContext } from './solution';
const extras: Record<string,unknown> = {};
Object.defineProperty(extras, '__proto__', {value:'literal', enumerable:true});
const output = composeContext({region:'r',attempt:0}, extras);
if (!Object.prototype.hasOwnProperty.call(output, '__proto__') || output['__proto__'] !== 'literal') throw new Error('own enumerable string key __proto__ lost');
