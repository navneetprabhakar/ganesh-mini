import { RouteEntry, RouteRegistry } from './solution';
let caught: unknown;
try { new RouteRegistry(new Array<RouteEntry>(1)); } catch (error) { caught = error; }
if (!(caught instanceof TypeError)) throw new Error('Missing route must not bypass constructor validation');
