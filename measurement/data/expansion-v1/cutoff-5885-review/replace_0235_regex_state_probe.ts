import {replaceMatches} from './solution';
const pattern = /a/g;
pattern.lastIndex = 2;
replaceMatches('aaa',pattern,'x');
console.log('lastIndex',pattern.lastIndex);
if(pattern.lastIndex !== 2) throw new Error('input RegExp state mutated');
