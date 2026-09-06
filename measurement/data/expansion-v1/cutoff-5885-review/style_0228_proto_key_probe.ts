import { createStyleRegistry, StyleObject } from './solution';
const palette: StyleObject = Object.create(null);
palette['__proto__'] = 'retain';
const actual = createStyleRegistry({ palette }, {}).getScheme().palette;
if (!Object.prototype.hasOwnProperty.call(actual, '__proto__') || actual['__proto__'] !== 'retain') {
  throw new Error('Own __proto__ style value lost during clone');
}
