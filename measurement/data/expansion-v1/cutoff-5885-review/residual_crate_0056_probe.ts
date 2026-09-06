import { CrateRegistry, type Crate } from './solution';
const crate: Crate = {id:'x',label:'X',capacity:0,tags:[]};
Object.defineProperty(crate, 'id', {enumerable:false});
const registry = new CrateRegistry();
registry.create(crate);
if (registry.get('x') === undefined) throw new Error('hidden required id lost; created crate cannot be retrieved by its exact id');
