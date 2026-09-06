import { ProfileRegistry, ProfileError } from './solution';
const registry = new ProfileRegistry([{ id: 'a', name: 'Alpha', badge: [7] }]);
let rejected = false;
try { registry.setBadge('a', new Array<number>(1)); }
catch (error) { rejected = error instanceof ProfileError && error.code === 'INVALID_BADGE'; }
if (!rejected) throw new Error('Missing badge byte must throw INVALID_BADGE');
if (JSON.stringify(registry.get('a').badge) !== '[7]') throw new Error('Failed operation changed state');
