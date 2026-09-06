import {ResponsiveMenu, type NavItem} from './solution';
let rejected=false;
try { new ResponsiveMenu(new Array<NavItem>(1),100); } catch(e) { if (!(e instanceof TypeError)) throw e; rejected=true; }
if(!rejected) throw new Error('Missing navigation item accepted');
