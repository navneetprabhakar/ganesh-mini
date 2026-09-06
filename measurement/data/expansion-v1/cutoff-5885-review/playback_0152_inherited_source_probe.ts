import { buildPlaybackPanel } from './solution';
const result = buildPlaybackPanel('constructor', [{ id: 'constructor', title: 'T' }], {});
if (result !== null) throw new Error('missing source resolved to Object.prototype.constructor; source type=' + typeof result.source);
