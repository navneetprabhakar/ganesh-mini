import { cleanCatalog } from './solution';
let threw = false;
try { cleanCatalog({ root: 'old', bundles: [] }, { root: '/x', allowedSuffixes: new Array<string>(1) }); } catch { threw = true; }
if (!threw) throw new Error('Missing suffix must not bypass dot-prefix validation');
