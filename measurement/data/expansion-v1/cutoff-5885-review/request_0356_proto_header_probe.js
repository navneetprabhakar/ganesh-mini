const buildRequestDescriptor = require('./solution');
const result = buildRequestDescriptor('x', '/', { headers: JSON.parse('{"__proto__":"value"}') });
if (!Object.prototype.hasOwnProperty.call(result.headers, '__proto__') || result.headers.__proto__ !== 'value') throw new Error('Own string header lost during copy');
