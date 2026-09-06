import { buildNavigationRows, NavigationEntry } from './solution';
let rejected = false;
try { buildNavigationRows(new Array<NavigationEntry>(1)); }
catch (error) { if (error instanceof TypeError) rejected = true; else throw error; }
if (!rejected) throw new Error('sparse navigation entries accepted');
