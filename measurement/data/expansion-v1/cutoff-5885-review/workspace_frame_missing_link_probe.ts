import { WorkspaceLink, renderWorkspaceFrame } from './solution';
let caught: unknown;
try { renderWorkspaceFrame({ logoText: 'Logo', activeRoute: '/', content: 'C', links: new Array<WorkspaceLink>(1) }); } catch (error) { caught = error; }
if (!(caught instanceof TypeError)) throw new Error('Missing link must reject malformed navigation');
