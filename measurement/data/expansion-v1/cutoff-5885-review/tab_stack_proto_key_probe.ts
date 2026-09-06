import { TabResetController } from './solution';
const stacks = JSON.parse('{"__proto__":["root"]}') as Record<string,string[]>;
const snapshot = new TabResetController('__proto__', stacks).snapshot();
if (!Object.prototype.hasOwnProperty.call(snapshot.stacks, '__proto__')) throw new Error('Valid tab key lost');
