import { buildViewTree } from './solution';
let caught: unknown;
try { buildViewTree([{ path: '/a', view: 'A', index: 0 as unknown as boolean }]); } catch (error) { caught = error; }
if (!(caught instanceof TypeError)) throw new Error('Numeric index flag must reject malformed specification');
