import { ShelfDocument, DocumentShelf } from './solution';
(async () => {
  const document: ShelfDocument = { id: 'a', title: 'Title', retired: true };
  Object.defineProperty(document, 'retired', { enumerable: false });
  const shelf = new DocumentShelf(async () => ({ documents: [document] }));
  await shelf.load();
  shelf.select('retired');
  if (shelf.rows().length !== 1) throw new Error('required retired flag lost, document misclassified');
})();
