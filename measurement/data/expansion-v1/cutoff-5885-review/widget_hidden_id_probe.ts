import { listWidgets, type Widget } from './solution';
const widget: Widget = {id:1, name:'A'};
Object.defineProperty(widget, 'id', {enumerable:false});
if (listWidgets([widget], 0, 1).data[0].id !== 1) throw new Error('Required widget ID lost');
