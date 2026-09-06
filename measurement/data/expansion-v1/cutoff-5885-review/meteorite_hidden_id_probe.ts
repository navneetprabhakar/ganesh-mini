import { MeteoriteCatalog, type MeteoriteRecord } from './solution';
const record: MeteoriteRecord = {id:1, label:'A', massGrams:0, note:null};
Object.defineProperty(record, 'id', {enumerable:false});
if (new MeteoriteCatalog([record]).getById(1)?.id !== 1) throw new Error('Required validated meteorite ID lost');
