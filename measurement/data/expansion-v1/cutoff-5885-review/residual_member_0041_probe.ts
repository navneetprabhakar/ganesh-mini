import { MemberDirectory, type Member } from './solution';
const member: Member = {id:'x', displayName:'X', contact:'c', registeredEpoch:0};
Object.defineProperty(member, 'id', {enumerable:false});
void (async () => {
 const directory = new MemberDirectory(); await directory.add(member);
 const output = await directory.get('x');
 if (output.id !== 'x') throw new Error('validated typed member loses non-enumerable required id');
})();
