import {OperatorDirectory,type OperatorRecord} from './solution';
const r:OperatorRecord={id:'a',handle:'A',contact:''};Object.defineProperty(r,'id',{enumerable:false});
if(new OperatorDirectory([r]).get('a')===null)throw new Error('Required operator ID lost during copy');
