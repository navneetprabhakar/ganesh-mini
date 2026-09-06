import { recordPoll, type CheckState } from './solution';
const state: CheckState = { phase: 'waiting', sessionId: 's', polls: 0 };
Object.defineProperty(state, 'phase', { value: 'waiting', enumerable: false });
const result = recordPoll(state, 'other', 'pending');
if (result.phase !== 'waiting') throw new Error('fresh unchanged state lost its phase');
