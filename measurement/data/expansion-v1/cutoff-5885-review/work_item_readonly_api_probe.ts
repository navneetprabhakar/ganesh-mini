import { WorkItem } from './solution';
const item: WorkItem = { id: 1, title: 'T', dueLabel: 'D' };
// @ts-expect-error Public API requires readonly id.
item.id = 2;
// @ts-expect-error Public API requires readonly title.
item.title = 'Changed';
// @ts-expect-error Public API requires readonly dueLabel.
item.dueLabel = 'Later';
