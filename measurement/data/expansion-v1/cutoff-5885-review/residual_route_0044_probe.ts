import { RouteEndpoint, type RouteDescriptor } from './solution';
const descriptor: RouteDescriptor = {scheme:'s',host:'h',port:80,accountId:0,groupId:0};
Object.defineProperty(descriptor, 'host', {enumerable:false});
const result = new RouteEndpoint(descriptor).getDescriptor();
if (result.host !== 'h') throw new Error('validated typed descriptor loses non-enumerable required host');
