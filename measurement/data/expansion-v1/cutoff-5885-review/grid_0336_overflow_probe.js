const { planGrid } = require('./solution');
const result = planGrid(Number.MAX_VALUE, Number.MAX_VALUE, Number.MAX_VALUE, ['x']);
if (result.rows.flat().join(',') !== 'x') throw new Error('Finite dimensions lost input ID through formula overflow: ' + JSON.stringify(result));
