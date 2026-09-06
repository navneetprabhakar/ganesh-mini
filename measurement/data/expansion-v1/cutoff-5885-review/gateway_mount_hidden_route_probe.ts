import { makeGatewayOptions, type MountPoint } from './solution';
const mount: MountPoint = {route:'/a', directory:'/srv/a'};
Object.defineProperty(mount, 'route', {enumerable:false});
if (makeGatewayOptions({mounts:[mount]}).mounts[0].route !== '/a') throw new Error('Required mount route lost');
