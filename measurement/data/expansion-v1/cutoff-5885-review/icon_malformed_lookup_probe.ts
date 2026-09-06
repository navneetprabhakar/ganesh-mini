import {IconDirectory} from './solution';
if(new IconDirectory(10).get(null as unknown as string)!==undefined) throw new Error('Malformed lookup must return undefined');
