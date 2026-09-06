import {PreferenceManager} from './solution';
const languages=['en'];languages.length=2;
let rejected=false;try { new PreferenceManager(languages,'en','#112233'); } catch(e) { if(!(e instanceof RangeError)) throw e;rejected=true; }
if(!rejected) throw new Error('Missing supported language accepted');
