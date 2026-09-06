import { WorkspaceGate } from './solution';
const accounts = Object.defineProperty({}, 'alice', { value: { secret: 's', modules: ['m'] }, enumerable: false });
(async () => {
  const result = await new WorkspaceGate(accounts).signIn('alice', 's');
  if (result.username !== 'alice') throw new Error('Copied account not available');
})();
