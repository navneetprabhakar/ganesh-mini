import { makeMemberSummary } from './solution';
const result = makeMemberSummary({ handle: 'h', contact: 'c', note: '', icon: null, roles: ['\u{1F600}', '\uE000'] });
if (result.roles[0] !== '\uE000') throw new Error('Role sorting must use code points, not UTF-16 code units');
