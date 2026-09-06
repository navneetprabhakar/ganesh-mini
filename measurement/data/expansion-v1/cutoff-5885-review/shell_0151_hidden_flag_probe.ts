import { shellReducer, startBusy, ShellState } from './solution';
const state: ShellState = { busy: false, panelVisible: true };
Object.defineProperty(state, 'panelVisible', { value: true, enumerable: false });
if (shellReducer(state, startBusy()).panelVisible !== true) throw new Error('Busy transition lost untouched panelVisible');
