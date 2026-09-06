import { visibleOutline, type OutlineNode } from './solution';
let root: OutlineNode = { id: '12000', label: 'n', kind: 'group', children: [] };
for (let i = 11999; i >= 0; i--) root = { id: String(i), label: 'n', kind: 'group', children: [root] };
try {
  const rows = visibleOutline([root], new Set());
  if (rows.length !== 1) throw new Error('collapsed outline should return root only');
} catch (error) {
  throw new Error('valid collapsed deep outline failed: ' + (error instanceof Error ? error.name + ': ' + error.message : String(error)));
}
