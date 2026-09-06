import {GalleryModel} from './solution';
let rejected=false;
try { new GalleryModel(new Array<string>(1)); } catch(e) { if (!(e instanceof TypeError)) throw e; rejected=true; }
if(!rejected) throw new Error('Single missing image accepted');
