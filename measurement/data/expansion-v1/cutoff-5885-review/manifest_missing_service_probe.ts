import { buildFeatureManifest } from './solution';
let caught: unknown;
try { buildFeatureManifest({ key: 'k', title: 'Title' }, new Array<string>(1)); } catch (error) { caught = error; }
if (!(caught instanceof TypeError)) throw new Error('Missing service must reject malformed text with TypeError');
