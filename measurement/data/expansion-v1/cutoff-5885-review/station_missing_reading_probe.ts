import {describeStations} from './solution';
let rejected=false;try { describeStations([{stationId:'s',readings:new Array<number>(1)}]); } catch(e) { if(!(e instanceof TypeError)) throw e;rejected=true; }
if(!rejected) throw new Error('Missing station reading accepted');
