const { reduceNumericInput } = require('./solution');
const result = reduceNumericInput({ value: 1e300, min: 0, max: 1e301, step: 1 }, { type: 'key', key: 'ArrowDown' });
if (result.value !== 1e300) throw new Error('Rounding overflow moved decrement to upper bound: ' + result.value);
