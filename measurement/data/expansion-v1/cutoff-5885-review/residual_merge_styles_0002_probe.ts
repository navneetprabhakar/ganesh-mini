import { mergeStyles, StyleProperties } from './solution';
const override: StyleProperties = { opacity: 0 };
Object.defineProperty(override, 'opacity', { value: 0, enumerable: false });
if (mergeStyles({ opacity: 1 }, override).opacity !== 0) throw new Error('supplied property ignored');
