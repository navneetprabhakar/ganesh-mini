import { Widget, applyWidgetCommand } from './solution';
const widget: Widget = { id: '', x: 0, y: 0, width: 20, height: 20, selected: false };
Object.defineProperty(widget, 'id', { enumerable: false });
const result = applyWidgetCommand(widget, { type: 'select', selected: true }, { width: 100, height: 100 });
if (result.id !== '') throw new Error('required empty identifier lost');
