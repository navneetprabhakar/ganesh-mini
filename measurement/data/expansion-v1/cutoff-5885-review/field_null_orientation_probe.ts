import { FieldOrientation, makeFieldPresentation } from './solution';
let caught: unknown;
try { makeFieldPresentation({ label: 'L', name: 'n', value: '', orientation: null as unknown as FieldOrientation }); } catch (error) { caught = error; }
if (!(caught instanceof TypeError)) throw new Error('Null is an invalid supplied orientation, not an omitted value');
