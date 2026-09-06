import { resolvePanel } from './solution';
const result = resolvePanel([{ id: 'x', titleKey: 'toString', detailKey: 'd', altKey: 'a' }], undefined, {});
if (result?.title !== 'toString') throw new Error('inherited method returned instead of missing-message fallback');
