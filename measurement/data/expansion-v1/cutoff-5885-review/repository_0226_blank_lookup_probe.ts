import {RecordRepository} from './solution';
const repository = new RecordRepository();
let rejected = false;
try { repository.find(' '); } catch(error) { if (!(error instanceof RangeError)) throw error; rejected=true; }
if (!rejected) throw new Error('blank lookup ID accepted');
