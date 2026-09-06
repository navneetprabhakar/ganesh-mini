import { Membership, MembershipManager } from './solution';
(async () => {
  const item: Membership = { id: 'm', service: 'Service', active: true, credits: 1 };
  Object.defineProperty(item, 'id', { enumerable: false });
  const manager = new MembershipManager({ count: async () => 1, at: async () => item, cancel: async () => {} });
  const rows = await manager.refresh('u');
  if (rows[0].id !== 'm') throw new Error('required membership id lost');
})();
