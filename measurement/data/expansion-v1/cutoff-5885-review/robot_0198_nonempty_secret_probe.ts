import { RobotConfigurationEditor } from './solution';
const editor = new RobotConfigurationEditor({nickname:'n', zone:'z', secret:'old'});
let calls = 0;
const ok = editor.rotateSecret('old', ' ', ' ', () => { calls++; return true; });
if (!ok || calls !== 1 || editor.getConfiguration().secret !== ' ') throw new Error('non-empty secret not stored');
