import { requestRecovery, type RecoveryUser } from './solution';
async function main() {
  const unrelated = {email:null, enabled:true, locked:false} as unknown as RecoveryUser;
  const result = await requestRecovery('a@b.com', [unrelated, {email:'a@b.com', enabled:true, locked:false}]);
  if (result !== 'Recovery instructions queued') throw new Error('Unrelated malformed email must be a nonmatch');
}
main().catch(error => { throw error; });
