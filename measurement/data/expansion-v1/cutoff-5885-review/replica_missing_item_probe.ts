import { ReplicaItem, applyReplicaChange } from './solution';
let threw = false;
try { applyReplicaChange({ revision: 0, items: [] }, { kind: 'replace', revision: 1, items: new Array<ReplicaItem>(1) }); } catch { threw = true; }
if (!threw) throw new Error('Missing replica item must not bypass ID validation');
