import { RevisionViewer, type ConfigurationRevision } from './solution';
const record = {key:'k', revision:1} as ConfigurationRevision;
Object.defineProperty(record,'payload',{value:'kept',enumerable:false});
const viewer = new RevisionViewer();
viewer.initialize([record]);
console.log(JSON.stringify(viewer.current()));
if (viewer.current()?.payload !== 'kept') throw new Error('selected payload lost');
