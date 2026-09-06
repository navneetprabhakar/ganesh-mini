import { ActionPanel, type ActionSpec } from './solution';
let rejected = false;
try { new ActionPanel(new Array<ActionSpec>(1)); }
catch (error) { rejected = error instanceof TypeError; }
if (!rejected) throw new Error('Missing action must throw TypeError');
