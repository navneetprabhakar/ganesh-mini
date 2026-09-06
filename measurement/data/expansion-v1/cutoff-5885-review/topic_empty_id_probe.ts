import { TopicRegistry } from './solution';
const registry = new TopicRegistry();
let rejected = 0;
for (const call of [() => registry.recipients(''), () => registry.publish('', 'message')]) {
  try { call(); } catch { rejected++; }
}
if (rejected !== 2) throw new Error(`empty topic accepted by ${2 - rejected} read operations`);
