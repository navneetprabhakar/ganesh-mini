import { Notebook, NotebookRowController } from './solution';
(async () => {
  const notebook: Notebook = { id: 'n', title: 'Title', summary: null };
  Object.defineProperty(notebook, 'id', { enumerable: false });
  const actions: any[] = [];
  const controller = new NotebookRowController(notebook, 'w', () => ({ selectedId: null, notebooks: [], saving: false }), a => actions.push(a), {
    rename: async () => {}, remove: async () => {}, list: async () => [notebook],
  });
  await controller.rename('New');
  if (actions[0].notebooks[0].id !== 'n') throw new Error('required notebook id lost');
})();
