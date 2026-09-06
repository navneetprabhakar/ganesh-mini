import { loadLocalizedResource } from './solution';
let synchronous = false;
let pending: Promise<unknown> | undefined;
try { pending = loadLocalizedResource({0: '/x'}, 0, {title: {key: ' '}, summary: ''}, {}); }
catch { synchronous = true; }
if (synchronous) throw new Error('metadata validation throws synchronously instead of rejecting returned Promise');
if (!pending) throw new Error('no Promise returned');
void pending.then(() => { throw new Error('expected rejection'); }, error => {
  if (!(error instanceof TypeError)) throw new Error('wrong rejection');
});
