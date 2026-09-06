import { CatalogInput, CatalogStore, registerCatalogItem } from './solution';
let inserted = false;
const store: CatalogStore = { insert: async record => { inserted = true; return { ...record, code: 1 }; } };
(async () => {
  let caught: unknown;
  try { await registerCatalogItem(store, { label: 'L', value: 'V', category: 'C', rank: null } as unknown as CatalogInput); }
  catch (error) { caught = error; }
  if (!caught || inserted) throw new Error('Supplied null rank silently defaulted and inserted despite safe-integer requirement');
})();
