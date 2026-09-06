import { renderContactStrip, ContactLink } from './solution';
const contacts = new Array<ContactLink>(1);
let rejected = false;
try { renderContactStrip('Contacts', contacts); } catch (error) { rejected = error instanceof TypeError; }
if (!rejected) throw new Error('Missing contact must not silently render as an empty valid list');
