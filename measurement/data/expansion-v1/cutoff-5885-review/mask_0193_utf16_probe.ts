import { maskCredential } from './solution';
const value = '\uD83D\uDE00abc';
const result = maskCredential(value);
console.log(JSON.stringify(result));
if (!result.ok || result.masked !== '*' + value.slice(-4)) throw new Error('not exactly final four UTF-16 units');
