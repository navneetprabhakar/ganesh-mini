import { PhraseBook } from './solution';
let caught = false;
try { new PhraseBook('toString', {}); }
catch (error) { if (!(error instanceof RangeError) || error.message !== 'Missing default locale') throw error; caught = true; }
if (!caught) throw new Error('Inherited Object method is not a supplied translation table');
