import { createGlyphDescriptor } from './solution';
const result = createGlyphDescriptor('a', { directory: '/' });
if (result.src !== '/a.svg') throw new Error('nonempty root directory was not normalized');
