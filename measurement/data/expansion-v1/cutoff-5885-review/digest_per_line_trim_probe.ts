import { digestText } from './solution';
const result = digestText('  First  \n  Second.  ', 'note');
if (result.summary !== 'First\nSecond') throw new Error('Every line must be trimmed before sentence extraction: ' + JSON.stringify(result.summary));
