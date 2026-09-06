import { RecordPresenter } from './solution';
const p = new RecordPresenter(id => ({ id, heading: 'H', details: 'D' }));
p.load('a');
try { p.load(' '); } catch (error) { if (!(error instanceof TypeError)) throw error; }
if (p.snapshot().record !== null || p.snapshot().error !== null) throw new Error('new invalid load attempt retained previous data');
