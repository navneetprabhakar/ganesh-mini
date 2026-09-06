import { SignInController, Credentials } from './solution';
const credentials: Credentials = { identifier: 'user', secret: 'secret' };
Object.defineProperty(credentials, 'identifier', { value: 'user', enumerable: false });
let received: Credentials | undefined;
const controller = new SignInController(async value => { received = value; return null; },
  { set: () => {} }, () => {}, () => {});
controller.submit(credentials).then(() => {
  if (received?.identifier !== 'user') throw new Error('Validated identifier lost before authenticate');
}).catch(error => { throw error; });
