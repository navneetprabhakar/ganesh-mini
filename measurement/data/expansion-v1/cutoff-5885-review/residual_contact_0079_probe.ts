import { selectContact, type ContactRecord } from './solution';
const record: ContactRecord = {key:'x',displayName:'X',address:'a',picture:null,active:false};
Object.defineProperty(record, 'address', {enumerable:false});
const result = selectContact([record], 'x');
if (result.kind !== 'found' || result.contact.address !== 'a') throw new Error('required non-enumerable address lost despite preserve every field contract');
