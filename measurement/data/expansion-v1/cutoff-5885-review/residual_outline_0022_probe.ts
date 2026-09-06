import { flattenOutline, type OutlineNode } from './solution';
let node: OutlineNode = {id: 'leaf', label: 'Leaf', children: []};
for (let i = 0; i < 10000; i++) node = {id: String(i), label: 'Node', children: [node]};
let count = 0;
try { count = flattenOutline([node]).length; }
catch (error) { throw new Error(`finite acyclic depth 10000 failed: ${error instanceof Error ? error.name : 'unknown'}`); }
if (count !== 10001) throw new Error('lost outline rows');
