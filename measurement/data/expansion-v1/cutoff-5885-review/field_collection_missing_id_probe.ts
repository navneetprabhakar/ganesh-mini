import {FieldCollection,type TextFieldState} from './solution';
let rejected=false;try { new FieldCollection(new Array<TextFieldState>(1)); } catch(e) { if(!(e instanceof RangeError)) throw e;rejected=true; }
if(!rejected) throw new Error('Missing field ID accepted');
