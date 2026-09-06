const { applyJobEvent } = require('./solution');
const state = Object.defineProperty({ requestId: 'new', data: [], error: null }, 'status', { value: 'running', enumerable: false });
const result = applyJobEvent(state, { type: 'FAIL', requestId: 'old', error: 'late' });
if (result.status !== 'running') throw new Error('Stale event copy lost unchanged status');
