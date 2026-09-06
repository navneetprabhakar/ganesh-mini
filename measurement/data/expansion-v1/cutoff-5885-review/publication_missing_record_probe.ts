import { Publication, PublicationCatalog } from './solution';
let rejected = false;
try { new PublicationCatalog(new Array<Publication>(1)); } catch (e) { if (!(e instanceof TypeError)) throw e; rejected = true; }
if (!rejected) throw new Error('missing publication accepted');
