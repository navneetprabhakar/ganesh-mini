import { ExchangeRecorder, type ExchangeRecord } from './solution';
const record: ExchangeRecord = {id:'e', channel:'c', verb:'V', status:200, elapsedTicks:0, breadcrumbLevel:'info'};
Object.defineProperty(record, 'id', {enumerable:false});
if (new ExchangeRecorder().transform(record, 0).id !== 'e') throw new Error('Required exchange ID lost');
