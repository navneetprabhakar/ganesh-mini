import { compileLayers, type Layer } from './solution';
const layer: Layer = {id:'A', depth:0, opacity:1};
Object.defineProperty(layer, 'id', {enumerable:false});
if (compileLayers([layer])[0].id !== 'A') throw new Error('Required layer ID lost');
