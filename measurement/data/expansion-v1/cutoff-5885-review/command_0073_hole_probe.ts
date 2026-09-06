import { validateCommandTree } from './solution';
const errors = validateCommandTree({ name: 'root', run() {}, children: new Array(1) });
if (JSON.stringify(errors) !== JSON.stringify(['root.children[0]: expected object'])) throw new Error('sparse child position bypassed node validation: ' + JSON.stringify(errors));
