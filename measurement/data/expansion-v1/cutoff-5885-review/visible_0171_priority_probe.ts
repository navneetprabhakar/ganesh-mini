import { chooseVisible } from './solution';
const result = chooseVisible([
  { id: 'a', width: 1, priority: 3, group: 'g' },
  { id: 'b', width: 1, priority: 8, group: 'g' },
  { id: 'high', width: 2, priority: 10 },
], 2);
if (result.visible.join(',') !== 'high') throw new Error('Group summed priorities instead of maximum: ' + result.visible.join(','));
