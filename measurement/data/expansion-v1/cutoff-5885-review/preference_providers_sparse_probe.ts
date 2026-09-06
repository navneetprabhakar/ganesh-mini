import { PreferenceForm } from './solution';
const form = new PreferenceForm({save:async () => {}}, {success() {},error() {}}, () => {});
let caught = false;
try { form.setProviders(new Array<string>(1)); }
catch (error) { if (!(error instanceof TypeError)) throw error; caught = true; }
if (!caught) throw new Error('Missing provider must be rejected');
