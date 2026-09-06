import { MemberRecord, queryMembers } from './solution';
const record: MemberRecord = { id: '1', contact: 'a@b', tier: 'gold' };
Object.defineProperty(record, 'tier', { value: 'gold', enumerable: false });
if (queryMembers([record], { contactText: '', page: 1, pageSize: 1 }).items[0].tier !== 'gold') throw new Error('Required member tier must survive copying');
