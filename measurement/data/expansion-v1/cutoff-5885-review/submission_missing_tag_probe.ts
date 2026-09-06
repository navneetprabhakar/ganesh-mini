import { SubmissionDesk } from './solution';
const desk = new SubmissionDesk();
let threw = false;
try { desk.create({ title: 'T', author: 'A', tags: new Array<string>(1) }); } catch { threw = true; }
if (!threw) throw new Error('Missing tag must not become a stored non-string');
if (desk.create({ title: 'T', author: 'A', tags: [] }).id !== 'S1') throw new Error('Invalid creation must not consume ID');
