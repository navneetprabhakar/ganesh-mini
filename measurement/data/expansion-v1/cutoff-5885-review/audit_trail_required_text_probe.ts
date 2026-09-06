import { AuditTrail } from './solution';
const entry = { id: 'a', sequence: 1, text: 'Original' };
Object.defineProperty(entry, 'text', { value: 'Original', enumerable: false });
const trail = new AuditTrail({ subscribe: () => () => {} }, [entry]);
if (trail.entries()[0].text !== 'Original') throw new Error('Required audit text lost');
