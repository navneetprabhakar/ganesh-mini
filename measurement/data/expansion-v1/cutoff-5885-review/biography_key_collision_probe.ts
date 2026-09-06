import {buildProfileView} from './solution';
const lines=buildProfileView({image:'x',biography:['A','A','A#2']}).lines;
if(new Set(lines.map(l=>l.key)).size !== lines.length) throw new Error('Biography keys are not unique');
