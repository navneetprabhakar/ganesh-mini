import {ChoiceModel,type ChoiceSpec} from './solution';
let rejected=false;try { new ChoiceModel('g',new Array<ChoiceSpec>(1)); } catch(e) { if(!(e instanceof RangeError)) throw e;rejected=true; }
if(!rejected) throw new Error('Missing choice value accepted');
