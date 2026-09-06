import { transitionDecision, DecisionState } from './solution';
const state: DecisionState = {open: false, message: 'keep', outcome: 'rejected'};
Object.defineProperty(state, 'message', {value: 'keep', enumerable: false});
if (transitionDecision(state, {type: 'accept'}).message !== 'keep') throw new Error('closed no-op lost message');
