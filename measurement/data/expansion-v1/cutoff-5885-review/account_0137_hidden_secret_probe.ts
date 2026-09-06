import { AccountManager, type Account } from './solution';
const a: Account = { firstName: 'A', lastName: 'B', secret: 's' };
Object.defineProperty(a, 'secret', { value: 's', enumerable: false });
const manager = new AccountManager(a);
if (!manager.changeSecret('s', 'new', 'new').ok) throw new Error('validated secret lost by constructor copy');
