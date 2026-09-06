import { splitInstructions, Instruction } from './solution';
const instruction: Instruction = { kind: 'query', name: 'status', arguments: [] };
Object.defineProperty(instruction, 'kind', { value: 'query', enumerable: false });
const result = splitInstructions([instruction]);
if (result.queries.length !== 1 || result.commands.length !== 0 || result.queries[0].kind !== 'query') {
  throw new Error('typed non-enumerable discriminant lost during copy');
}
