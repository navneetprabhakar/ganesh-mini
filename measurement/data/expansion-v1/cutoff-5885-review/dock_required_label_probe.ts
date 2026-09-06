import { createDockState, reduceDock } from './solution';
const state = createDockState();
Object.defineProperty(state.actions[0], 'label', { value: 'Close', enumerable: false });
const next = reduceDock(state, 'dismiss');
if (next.actions[0].label !== 'Close') throw new Error('Reduction must preserve existing action label');
