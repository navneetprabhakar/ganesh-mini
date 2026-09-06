import { ActionShelfRegistry } from './solution';
const action = { commandId: 'run' };
Object.defineProperty(action, 'commandId', { value: 'run', enumerable: false });
const registry = new ActionShelfRegistry();
registry.register('canvas/tools', action);
if (registry.list('canvas/tools')[0].commandId !== 'run') throw new Error('Required command ID lost');
