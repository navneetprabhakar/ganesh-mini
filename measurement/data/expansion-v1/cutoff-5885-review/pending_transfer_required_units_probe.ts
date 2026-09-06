import { PendingTransfer, PendingTransferService } from './solution';
(async () => {
  const row: PendingTransfer = { id: 'a', units: 1, cost: 2, weight: 3 };
  Object.defineProperty(row, 'units', { enumerable: false });
  const service = new PendingTransferService({ read: async () => [row, { id: 'b', units: 2, cost: 2, weight: 3 }] });
  const rows = await service.query({ limit: 2, offset: 0, field: 'units', direction: 'asc' });
  if (rows[0].id !== 'a' || rows[0].units !== 1) throw new Error('required units lost before sorting');
})();
