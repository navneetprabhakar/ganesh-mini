import { CredentialRecord, authenticateLocal } from './solution';
const record: CredentialRecord = { userId: 'u', displayName: 'A', email: 'a@b', avatarKey: 'x', password: 'p' };
Object.defineProperty(record, 'userId', { value: 'u', enumerable: false });
if (authenticateLocal([record], 'a@b', 'p').userId !== 'u') throw new Error('Valid required user ID must survive copying');
