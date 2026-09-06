import { Memo, Journal } from './solution';
const journal = new Journal();
let current = new Memo(0, '', ''); journal.add(current);
for (let id = 1; id <= 12000; id++) { const child = new Memo(id, '', ''); current.addChild(child); current = child; }
try { if (journal.find(12000) !== current) throw new Error('Deep descendant not returned'); }
catch (error) { const e = error as Error; throw new Error(e.name + ': ' + e.message); }
