import { normalizeAssignment, type AssignmentInput } from './solution';
const input = {organization:null} as unknown as AssignmentInput;
if (normalizeAssignment(input).organization !== 'Unknown organization') throw new Error('Null text field must use fallback');
