import { updateAccountMenu, type AccountMenuState } from './solution';
const state: AccountMenuState = {open:false,signedIn:true,email:'e',displayName:'d',destination:null};
Object.defineProperty(state, 'email', {enumerable:false});
const output = updateAccountMenu(state, {type:'toggle'});
if (output.email !== 'e') throw new Error('toggle loses non-enumerable profile field instead of flipping open only');
