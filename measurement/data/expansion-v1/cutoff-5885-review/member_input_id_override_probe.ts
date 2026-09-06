import { NewMember, MemberDirectory } from './solution';
const input: NewMember & { id: string } = { handle: 'a', contact: 'a@b', secret: '123456', fullName: 'A', id: 'injected' };
if (new MemberDirectory().create(input).id !== 'm1') throw new Error('Caller extra field must not override deterministic generated member ID');
