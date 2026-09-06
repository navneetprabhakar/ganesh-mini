import { PassRegistry, createObserverPass } from './solution';
const registry = new PassRegistry();
let innerId = '';
const outer = createObserverPass(registry, { handle: 'outer' }, {
  publish(): void {
    innerId = createObserverPass(registry, { handle: 'inner' }, { publish(): void {} }).id;
  }
});
if (outer.id === innerId || registry.list().length !== 2) throw new Error('Successful nested issuance must not overwrite a pass or reuse its ID');
