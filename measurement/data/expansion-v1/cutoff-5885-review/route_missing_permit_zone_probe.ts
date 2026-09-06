import { resolveRoute } from './solution';
const zones = ['z']; zones.length = 2;
let threw = false;
try { resolveRoute({ ownerId: 'o', zones }, [{ id: 'r', zone: 'z', priority: 0, enabled: true }]); } catch { threw = true; }
if (!threw) throw new Error('Missing permit zone must not bypass normalization');
