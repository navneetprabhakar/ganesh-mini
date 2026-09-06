import { transitionQueue } from './solution';
let caught = false;
try { transitionQueue({trackIds:new Array<string>(1), index:0, playing:false}, {type:'toggle'}); }
catch (error) { if (!(error instanceof RangeError)) throw error; caught = true; }
if (!caught) throw new Error('Missing stored track ID must be rejected');
