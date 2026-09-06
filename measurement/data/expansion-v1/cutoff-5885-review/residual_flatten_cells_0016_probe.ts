import { flattenCellText } from './solution';
let value: unknown = {text: 'x'};
for (let i = 0; i < 10000; i++) value = [value];
let result: string[] | undefined;
let errorName: string | undefined;
try { result = flattenCellText(value); } catch (error) { errorName = error instanceof Error ? error.name : String(error); }
if (errorName !== undefined || result?.length !== 1 || result[0] !== 'x') throw new Error('finite acyclic depth failed: ' + errorName);
