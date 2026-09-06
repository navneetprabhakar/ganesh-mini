import { DirectoryEntry, pageDirectory } from './solution';
let rejected = false;
try { pageDirectory(new Array<DirectoryEntry>(1), 1, 10); }
catch (error) { if (error instanceof TypeError) rejected = true; else throw error; }
if (!rejected) throw new Error('sparse directory not rejected');
