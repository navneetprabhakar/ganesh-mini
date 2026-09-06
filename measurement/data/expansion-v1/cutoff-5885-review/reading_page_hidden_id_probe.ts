import { queryReadings, type Reading } from './solution';
const reading: Reading = {id:'X', value:1, recordedAt:0, station:'A'};
Object.defineProperty(reading, 'id', {enumerable:false});
if (queryReadings([reading], {page:1, pageSize:1, sortBy:'id', direction:'asc'}).items[0].id !== 'X') throw new Error('Required reading ID lost');
