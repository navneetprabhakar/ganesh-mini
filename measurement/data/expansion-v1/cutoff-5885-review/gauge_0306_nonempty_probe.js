const GaugeCard = require('./solution');
const gauge = new GaugeCard(' ', 'red');
if (gauge.commands()[1].surfaceId !== ' ') throw new Error('Non-empty surface ID not preserved');
