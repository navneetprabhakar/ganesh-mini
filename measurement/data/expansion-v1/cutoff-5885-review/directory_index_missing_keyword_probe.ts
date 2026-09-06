import { DirectoryIndex } from './solution';
let caught: unknown;
try { new DirectoryIndex([{ id: 'a', label: 'A', keywords: new Array<string>(1) }]); } catch (error) { caught = error; }
if (!(caught instanceof TypeError)) throw new Error('Missing keyword must be rejected');
