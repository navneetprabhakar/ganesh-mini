import {PlaylistStore} from './solution';
let rejected=false; try { new PlaylistStore(new Array<string>(1)); } catch(e) { if(!(e instanceof TypeError)) throw e; rejected=true; }
if(!rejected) throw new Error('Missing track accepted');
