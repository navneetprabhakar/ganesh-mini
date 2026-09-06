import { collectDependencies } from './solution';
let result: string[];
try { result = collectDependencies({}, ['constructor']); }
catch (error) { throw new Error(`absent graph root constructor must be leaf, got ${error instanceof Error ? error.name : 'unknown'}`); }
if (result.length !== 0) throw new Error('absent root not treated as leaf');
