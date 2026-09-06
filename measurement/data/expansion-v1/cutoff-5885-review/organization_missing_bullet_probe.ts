import { renderOrganizationBrief } from './solution';
let rejected = false;
try { renderOrganizationBrief({ title: 'T', summary: 'S', sections: [{ heading: 'H', body: 'B', bullets: new Array<string>(1) }] }); }
catch (e) { if (!(e instanceof TypeError)) throw e; rejected = true; }
if (!rejected) throw new Error('missing nonempty bullet accepted');
