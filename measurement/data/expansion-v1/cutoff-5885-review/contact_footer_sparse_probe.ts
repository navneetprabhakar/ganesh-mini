import { renderContactFooter, type ContactLink } from './solution';
let caught = false;
try { renderContactFooter(new Array<ContactLink>(1), 'Org', 2026); }
catch (error) { if (!(error instanceof RangeError)) throw error; caught = true; }
if (!caught) throw new Error('Malformed missing contact link must be rejected');
