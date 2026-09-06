import { createTileView } from './solution';
let rejected = false;
try { createTileView({caption: 'valid', assetPath: 'valid', markers: 2 ** 32}); }
catch (error) { if (error instanceof RangeError) rejected = true; else throw error; }
if (!rejected) throw new Error('markers above 31 accepted through 32-bit truncation');
