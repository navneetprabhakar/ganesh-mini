import { mergePreferences } from './solution';
const input = JSON.parse('{"__proto__":{"kept":true}}');
const result = mergePreferences([input]);
if (!Object.prototype.hasOwnProperty.call(result, '__proto__')) throw new Error('Own enumerable __proto__ key lost');
