import {generateLabels} from './solution';
const labels=generateLabels(['A','A','A-2']);
if(new Set(labels.map(x=>x.id)).size!==labels.length) throw new Error('Generated label IDs collide');
