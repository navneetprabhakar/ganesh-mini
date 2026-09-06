import { ConstellationStore } from './solution';
const store = new ConstellationStore();
let rejected = false;
try { store.create({name: 'valid', stars: new Array<string>(1)}); }
catch (error) { if (error instanceof TypeError) rejected = true; else throw error; }
if (!rejected || store.findAll().length !== 0) throw new Error('sparse stars accepted into repository');
