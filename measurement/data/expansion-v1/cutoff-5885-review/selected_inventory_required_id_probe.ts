import { InventoryItem, selectInventory } from './solution';
const item: InventoryItem = { id: 1, title: 'A', section: 'Books', cost: 1 };
Object.defineProperty(item, 'id', { value: 1, enumerable: false });
if (selectInventory([item], { sections: [], page: 1, pageSize: 1 }).data[0].id !== 1) throw new Error('Required inventory ID must survive copying');
