import { sumNumericLeaves } from './solution';
let value: unknown = 1;
for (let i = 0; i < 6000; i++) value = [value];
let errorName: string | undefined;
let result: number | undefined;
try { result = sumNumericLeaves(value); } catch (error) { errorName = error instanceof Error ? error.name : String(error); }
if (errorName !== undefined || result !== 1) throw new Error('finite acyclic nesting failed: ' + errorName);
