import { MessageDeck } from './solution';
let caught = false;
try { new MessageDeck(new Array<string>(1), [], ''); }
catch (error) { if (!(error instanceof RangeError)) throw error; caught = true; }
if (!caught) throw new Error('Missing message must be rejected');
