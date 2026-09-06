import { matchPath } from './solution';
const result = matchPath([{pattern: '/:__proto__', destination: 'd'}], '/value');
if (!result || !Object.prototype.hasOwnProperty.call(result.params, '__proto__') || result.params['__proto__'] !== 'value') {
  throw new Error('valid parameter name __proto__ was lost');
}
