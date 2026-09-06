import { updateSession, Member } from './solution';
const member: Member = { id: 'id', displayName: 'Name', avatar: null };
Object.defineProperty(member, 'displayName', { value: 'Name', enumerable: false });
const result = updateSession({ member: null, pending: false, revision: 0 }, { type: 'accept', member });
if (result.member?.displayName !== 'Name') throw new Error('Accepted member loses validated displayName');
