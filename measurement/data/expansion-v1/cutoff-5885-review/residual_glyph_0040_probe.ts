import { createGlyphRenderer } from './solution';
const attributes: Record<string,string> = {};
Object.defineProperty(attributes, '__proto__', {value:'literal', enumerable:true});
const output = createGlyphRenderer({pathData:'M0',viewBox:'0 0 1 1'})({attributes});
if (!Object.prototype.hasOwnProperty.call(output.attributes, '__proto__') || output.attributes['__proto__'] !== 'literal') throw new Error('own caller attribute __proto__ lost');
