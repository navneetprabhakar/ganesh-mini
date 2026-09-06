import { encodeTags, TagValue } from './solution';
let rejected = false;
try { encodeTags(new Array<TagValue>(1)); }
catch (error) { if (error instanceof TypeError) rejected = true; else throw error; }
if (!rejected) throw new Error('sparse tag values serialized instead of rejected');
