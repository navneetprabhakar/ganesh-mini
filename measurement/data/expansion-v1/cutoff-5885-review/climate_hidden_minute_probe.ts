import { ClimateArchive, type Reading } from './solution';
const reading: Reading = {minute:0, temperature:20, humidity:50, code:'A'};
Object.defineProperty(reading, 'minute', {enumerable:false});
if (new ClimateArchive([reading]).latest()?.minute !== 0) throw new Error('Required minute lost');
