const { flattenConfig } = require('./solution');
const result = flattenConfig({ leaf: [JSON.parse('{"__proto__":7}')] });
const clone = result[0].value[0];
if (!Object.prototype.hasOwnProperty.call(clone, '__proto__') || clone.__proto__ !== 7) throw new Error('Own __proto__ JSON leaf field lost during clone');
